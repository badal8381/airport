# Copyright (c) 2025, Unity and contributors
# For license information, please see license.txt

import frappe  # noqa: I001
from frappe.model.document import Document
from frappe.utils import today, add_months, getdate, add_days
from dateutil.relativedelta import relativedelta


class RentContract(Document):
	def before_insert(self):
		"""Set default rent amount from settings if not provided"""
		if not self.rent_amount:
			settings = frappe.get_single("Airport Shop Settings")
			if settings and settings.default_rent_amount:
				self.rent_amount = settings.default_rent_amount

	def validate(self):
		"""Generate or regenerate payment schedule on save"""
		# Only generate if we have all required fields
		if not self.start_date or not self.end_date or not self.rent_amount:
			return

		# Check if schedule needs to be generated
		needs_generation = False

		if self.is_new():
			# New contract - generate schedule if not already populated
			needs_generation = len(self.payment_schedule) == 0
		else:
			# Existing contract - regenerate only if dates or amount changed
			if self.has_value_changed("start_date") or self.has_value_changed("end_date") or self.has_value_changed("rent_amount"):
				needs_generation = True

		if needs_generation:
			# Clear existing schedule
			self.payment_schedule = []
			self.generate_payment_schedule()

	def generate_payment_schedule(self):
		"""
		Auto-generate monthly payment schedule based on contract start and end dates
		Payment due date follows the day of contract start date
		Example: If contract starts on 15th, rent due on 15th of each month
		"""
		if not self.start_date or not self.end_date or not self.rent_amount:
			frappe.msgprint("Cannot generate payment schedule: start_date, end_date, and rent_amount are required")
			return

		start_date = getdate(self.start_date)
		end_date = getdate(self.end_date)

		if start_date > end_date:
			frappe.throw("Start date cannot be after end date")
			return

		# Calculate number of months
		months = 0
		current_date = start_date

		while current_date <= end_date:
			# Create schedule entry for this month
			self.append("payment_schedule", {
				"due_date": current_date,
				"scheduled_amount": self.rent_amount,
				"payment_status": "Pending",
				"paid_amount": 0,
				"rent_payment": None,
				"remarks": ""
			})

			# Move to next month on the same day
			months += 1
			try:
				# Use relativedelta to handle month-end edge cases properly
				current_date = start_date + relativedelta(months=months)
			except Exception as e:
				# Fallback for edge cases
				frappe.logger().error(f"Error calculating next month: {str(e)}")
				current_date = add_months(start_date, months)

			# If next due date exceeds contract end date, stop
			if current_date > end_date:
				break

		frappe.msgprint(f"Generated {len(self.payment_schedule)} payment schedule entries")


def send_monthly_rent_reminders():
	"""
	Monthly scheduled task to:
	1. Create Rent Payment records with 'Pending' status for upcoming due dates
	2. Send rent reminder emails to tenants
	Runs on the 1st of every month
	"""
	# Check if rent reminders are enabled
	settings = frappe.get_single("Airport Shop Settings")
	if not settings.enable_rent_reminders:
		frappe.logger().info("Rent reminders are disabled in Airport Shop Settings")
		return

	# Get all active rent contracts
	active_contracts = frappe.get_all(
		"Rent Contract",
		filters={
			"status": "Active",
			"end_date": [">=", today()]
		},
		fields=["name", "tenant", "shop", "rent_amount", "start_date", "end_date"]
	)

	today_date = getdate(today())

	for contract_data in active_contracts:
		try:
			contract = frappe.get_doc("Rent Contract", contract_data.name)
			tenant = frappe.get_doc("Tenant", contract.tenant)

			# Check payment schedule for current month's due date
			if contract.payment_schedule:
				for schedule_entry in contract.payment_schedule:
					due_date = getdate(schedule_entry.due_date)

					# Check if payment is due this month and still pending
					if (due_date.month == today_date.month and
						due_date.year == today_date.year and
						schedule_entry.payment_status in ["Pending", "Overdue"]):

						# Check if Rent Payment already exists for this schedule entry
						existing_payment = frappe.db.exists(
							"Rent Payment",
							{
								"contract": contract.name,
								"payment_date": due_date,
								"status": "Pending"
							}
						)

						if not existing_payment:
							# Create Rent Payment with Pending status
							rent_payment = frappe.get_doc({
								"doctype": "Rent Payment",
								"contract": contract.name,
								"shop": contract.shop,
								"tenant": contract.tenant,
								"amount": schedule_entry.scheduled_amount,
								"payment_method": "Bank Transfer",  # Default method
								"payment_date": due_date,
								"status": "Pending"
							})
							rent_payment.insert(ignore_permissions=True)
							frappe.logger().info(f"Created pending rent payment {rent_payment.name} for contract {contract.name}")

			# Prepare and send email reminder
			subject = f"Rent Reminder - {contract.shop}"
			message = f"""
				<p>Dear {tenant.tenant_name},</p>

				<p>This is a friendly reminder that your monthly rent for <b>{contract.shop}</b> is due.</p>

				<p><b>Rent Details:</b></p>
				<ul>
					<li>Shop: {contract.shop}</li>
					<li>Monthly Rent: {frappe.format_value(contract.rent_amount, {'fieldtype': 'Currency'})}</li>
					<li>Contract Period: {frappe.format_value(contract.start_date, {'fieldtype': 'Date'})} to {frappe.format_value(contract.end_date, {'fieldtype': 'Date'})}</li>
				</ul>

				<p>A payment record has been created in the system. Please ensure timely payment to avoid any inconvenience.</p>

				<p>Thank you,<br>
				Airport Management</p>
			"""

			# Send email
			frappe.sendmail(
				recipients=[tenant.email],
				subject=subject,
				message=message,
				reference_doctype="Rent Contract",
				reference_name=contract.name
			)

			frappe.logger().info(f"Rent reminder sent to {tenant.email} for contract {contract.name}")

		except Exception as e:
			frappe.logger().error(f"Error processing rent reminder for contract {contract_data.name}: {str(e)}")
			continue

	frappe.db.commit()


def mark_overdue_payments():
	"""
	Daily scheduled task to mark overdue payment schedule entries
	Updates payment_status from 'Pending' to 'Overdue' for past due dates
	"""
	# Get all active contracts with payment schedules
	active_contracts = frappe.get_all(
		"Rent Contract",
		filters={
			"status": "Active"
		},
		fields=["name"]
	)

	today_date = today()
	updated_count = 0

	for contract_data in active_contracts:
		try:
			contract = frappe.get_doc("Rent Contract", contract_data.name)

			if not contract.payment_schedule:
				continue

			schedule_updated = False

			for schedule_entry in contract.payment_schedule:
				# Mark as overdue if:
				# 1. Due date has passed
				# 2. Status is still Pending
				if schedule_entry.payment_status == "Pending" and getdate(schedule_entry.due_date) < getdate(today_date):
					schedule_entry.payment_status = "Overdue"
					schedule_updated = True
					updated_count += 1

			if schedule_updated:
				contract.save(ignore_permissions=True)
				frappe.logger().info(f"Marked overdue payments for contract {contract.name}")

		except Exception as e:
			frappe.logger().error(f"Error marking overdue payments for contract {contract_data.name}: {str(e)}")
			continue

	frappe.db.commit()
	frappe.logger().info(f"Marked {updated_count} payment schedule entries as overdue")
