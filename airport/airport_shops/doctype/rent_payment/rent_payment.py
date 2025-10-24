# Copyright (c) 2025, Unity and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, flt


class RentPayment(Document):
	def after_insert(self):
		"""Reconcile payment with payment schedule"""
		self.reconcile_with_schedule()

	def on_update(self):
		"""When status changes to Paid, update the payment schedule"""
		if self.has_value_changed("status") and self.status == "Paid":
			self.reconcile_with_schedule()

	def reconcile_with_schedule(self):
		"""
		Find matching payment schedule entry and update it
		Matches by contract and closest due date to payment date
		Only updates schedule when payment status is "Paid"
		"""
		if not self.contract:
			return

		# Only reconcile if status is Paid
		if self.status != "Paid":
			return

		# Get the contract document
		contract = frappe.get_doc("Rent Contract", self.contract)

		if not contract.payment_schedule:
			return

		# Find the closest payment schedule entry to this payment date
		payment_date = getdate(self.payment_date)
		closest_entry = None
		min_difference = None

		for idx, schedule_entry in enumerate(contract.payment_schedule):
			due_date = getdate(schedule_entry.due_date)
			difference = abs((payment_date - due_date).days)

			# Only consider pending, overdue, or partially paid entries
			if schedule_entry.payment_status in ["Pending", "Overdue", "Partially Paid"]:
				if closest_entry is None or difference < min_difference:
					closest_entry = schedule_entry
					min_difference = difference
					schedule_entry.idx = idx

		# Update the closest schedule entry
		if closest_entry:
			paid_amount = flt(closest_entry.paid_amount) + flt(self.amount)
			scheduled_amount = flt(closest_entry.scheduled_amount)

			# Determine payment status
			if paid_amount >= scheduled_amount:
				payment_status = "Paid"
			elif paid_amount > 0:
				payment_status = "Partially Paid"
			else:
				payment_status = "Pending"

			# Update schedule entry
			contract.payment_schedule[closest_entry.idx].paid_amount = paid_amount
			contract.payment_schedule[closest_entry.idx].payment_status = payment_status
			contract.payment_schedule[closest_entry.idx].rent_payment = self.name

			# Save the contract
			contract.save(ignore_permissions=True)

			# Store reference to schedule entry
			self.db_set("payment_schedule_entry", f"{self.contract}-{closest_entry.idx}", update_modified=False)

			frappe.logger().info(f"Payment {self.name} reconciled with schedule entry {closest_entry.idx} of contract {self.contract}")
