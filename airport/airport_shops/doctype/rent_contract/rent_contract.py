# Copyright (c) 2025, Unity and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, add_months, getdate


class RentContract(Document):
	def before_insert(self):
		"""Set default rent amount from settings if not provided"""
		if not self.rent_amount:
			settings = frappe.get_single("Airport Shop Settings")
			if settings and settings.default_rent_amount:
				self.rent_amount = settings.default_rent_amount


def send_monthly_rent_reminders():
	"""
	Monthly scheduled task to send rent reminder emails to tenants
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

	for contract in active_contracts:
		try:
			# Get tenant details
			tenant = frappe.get_doc("Tenant", contract.tenant)

			# Prepare email content
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

				<p>Please ensure timely payment to avoid any inconvenience.</p>

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
			frappe.logger().error(f"Error sending rent reminder for contract {contract.name}: {str(e)}")
			continue

	frappe.db.commit()
