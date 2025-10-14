# Copyright (c) 2025, Unity and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
	def before_save(self):
		"""Auto-populate full name from first and last name"""
		parts = [self.first_name]
		if self.last_name:
			parts.append(self.last_name)
		self.full_name = " ".join(parts)
