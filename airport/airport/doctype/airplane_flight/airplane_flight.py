# Copyright (c) 2025, Unity and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		"""Set status to Completed when flight is submitted"""
		self.status = "Completed"

	def on_update(self):
		"""Detect gate number changes and trigger background job"""
		# Check if gate_number has changed
		if self.has_value_changed("gate_number"):
			old_gate = self.get_doc_before_save().gate_number if self.get_doc_before_save() else None
			new_gate = self.gate_number

			frappe.logger().info(f"Gate number changed for flight {self.name}: {old_gate} -> {new_gate}")

			# Enqueue background job to update all related tickets
			frappe.enqueue(
				update_ticket_gate_numbers,
				flight=self.name,
				new_gate_number=new_gate,
				queue="default",
				timeout=300,
				is_async=True
			)

			frappe.msgprint(
				f"Gate number updated to {new_gate}. Ticket gate numbers are being updated in the background.",
				indicator="blue",
				alert=True
			)


def update_ticket_gate_numbers(flight, new_gate_number):
	"""
	Background job to update gate numbers in all tickets for a given flight
	This runs asynchronously to avoid blocking the UI
	"""
	try:
		# Get all tickets for this flight that are not cancelled
		tickets = frappe.get_all(
			"Airplane Ticket",
			filters={
				"flight": flight,
				"docstatus": ["<", 2]  # Not cancelled
			},
			fields=["name"]
		)

		frappe.logger().info(f"Updating gate numbers for {len(tickets)} tickets of flight {flight}")

		# Update each ticket's gate number
		for ticket in tickets:
			frappe.db.set_value(
				"Airplane Ticket",
				ticket.name,
				"gate_number",
				new_gate_number,
				update_modified=True
			)

		frappe.db.commit()

		# Log success
		frappe.logger().info(
			f"Successfully updated gate numbers to {new_gate_number} for {len(tickets)} tickets of flight {flight}"
		)

		# Create a notification for the user
		frappe.publish_realtime(
			"msgprint",
			f"Successfully updated gate numbers for {len(tickets)} tickets to {new_gate_number}",
			user=frappe.session.user
		)

	except Exception as e:
		frappe.logger().error(f"Error updating ticket gate numbers for flight {flight}: {str(e)}")
		frappe.db.rollback()
		raise
