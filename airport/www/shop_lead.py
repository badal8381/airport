import frappe
from frappe import _


def get_context(context):
	"""
	Get context for shop lead form page
	"""
	context.no_cache = 1

	# Get shop name from query parameter
	shop_name = frappe.form_dict.get("shop")

	if shop_name:
		try:
			shop = frappe.get_doc("Shop", shop_name)
			context.shop = shop
			context.shop_name = shop_name
		except frappe.DoesNotExistError:
			frappe.throw(_("Shop not found"))
	else:
		context.shop = None
		context.shop_name = None

	context.title = "Express Interest"

	return context


@frappe.whitelist(allow_guest=True)
def create_shop_lead(**kwargs):
	"""
	API method to create a shop lead from web form
	"""
	try:
		# Create new Shop Lead document
		lead = frappe.get_doc({
			"doctype": "Shop Lead",
			"full_name": kwargs.get("full_name"),
			"email": kwargs.get("email"),
			"phone": kwargs.get("phone"),
			"company_name": kwargs.get("company_name"),
			"shop_interest": kwargs.get("shop_interest"),
			"message": kwargs.get("message"),
			"status": "New",
			"lead_date": frappe.utils.today()
		})

		lead.insert(ignore_permissions=True)
		frappe.db.commit()

		return {
			"success": True,
			"message": "Shop lead created successfully",
			"lead_name": lead.name
		}

	except Exception as e:
		frappe.logger().error(f"Error creating shop lead: {str(e)}")
		frappe.throw(_("Error creating shop lead. Please try again."))
