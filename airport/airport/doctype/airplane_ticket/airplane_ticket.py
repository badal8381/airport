# Copyright (c) 2025, Unity and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
	def get_list_query(query):
		pass

	def get_indicator(doc):
		"""Return indicator for list view based on status"""
		status_color = {
			"Booked": "blue",
			"Checked-In": "orange",
			"Boarded": "green"
		}
		return status_color.get(doc.status, "gray")
