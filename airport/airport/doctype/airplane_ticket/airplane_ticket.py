# Copyright (c) 2025, Unity and contributors
# For license information, please see license.txt

import random
import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
	def get_list_query(query):
		pass

	def before_insert(self):
		"""Auto-assign seat before inserting into database"""
		if not self.seat:
			self.seat = self.generate_seat_number()

	def generate_seat_number(self):
		"""Generate a random seat number in format: <number><letter>"""
		seat_number = random.randint(1, 99)

		seat_letter = random.choice(['A', 'B', 'C', 'D', 'E'])

		return f"{seat_number}{seat_letter}"

	def validate(self):
		"""Validate ticket data and calculate total amount"""
		self.check_duplicate_addons()

		self.calculate_total_amount()

	def calculate_total_amount(self):
		"""Calculate total amount from flight price and add-ons"""
		total = self.flight_price or 0

		if self.add_ons:
			for addon in self.add_ons:
				total += addon.amount or 0

		self.total_amount = total

	def check_duplicate_addons(self):
		"""Check for duplicate add-on items and raise error if found"""
		if not self.add_ons:
			return

		seen_items = []

		for addon in self.add_ons:
			if addon.item in seen_items:
				frappe.throw(f"Duplicate add-on item: {addon.item}")
			seen_items.append(addon.item)

	def before_submit(self):
		"""Validate before submission"""
		if self.status != "Boarded":
			frappe.throw("Ticket can only be submitted if status is 'Boarded'")

	def get_indicator(doc):
		"""Return indicator for list view based on status"""
		status_color = {
			"Booked": "blue",
			"Checked-In": "orange",
			"Boarded": "green"
		}
		return status_color.get(doc.status, "gray")
