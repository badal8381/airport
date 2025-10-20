# Copyright (c) 2025, Unity and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShopLead(Document):
	def after_insert(self):
		"""Send notification email to admin after lead submission"""
		self.send_notification_email()

	def send_notification_email(self):
		"""Send email notification to shop manager"""
		try:
			# Get shop details
			shop = frappe.get_doc("Shop", self.shop_interest)

			subject = f"New Shop Lead: {self.full_name} - {shop.shop_number}"
			message = f"""
				<h3>New Shop Lead Received</h3>

				<p>A new inquiry has been received for shop <b>{shop.shop_number}</b>.</p>

				<h4>Lead Details:</h4>
				<ul>
					<li><b>Name:</b> {self.full_name}</li>
					<li><b>Email:</b> {self.email}</li>
					<li><b>Phone:</b> {self.phone}</li>
					{f"<li><b>Company:</b> {self.company_name}</li>" if self.company_name else ""}
					<li><b>Shop Interest:</b> {shop.shop_number} ({shop.shop_name or 'N/A'})</li>
				</ul>

				{f"<p><b>Message:</b><br>{self.message}</p>" if self.message else ""}

				<p>Please follow up with this lead at your earliest convenience.</p>

				<p><a href="{frappe.utils.get_url()}/app/shop-lead/{self.name}">View Lead in System</a></p>
			"""

			# Send to System Managers
			system_managers = frappe.get_all(
				"User",
				filters={"enabled": 1},
				fields=["email"]
			)

			if system_managers:
				recipients = [user.email for user in system_managers if user.email]

				frappe.sendmail(
					recipients=recipients,
					subject=subject,
					message=message,
					reference_doctype=self.doctype,
					reference_name=self.name
				)

		except Exception as e:
			frappe.logger().error(f"Error sending shop lead notification: {str(e)}")
