# Copyright (c) 2025, Unity and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		"""Set status to Completed when flight is submitted"""
		self.status = "Completed"
