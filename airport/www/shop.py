import frappe
from frappe import _


def get_context(context):
	"""
	Get context for individual shop detail page
	URL pattern: /shop?id=<shop-name>
	"""
	context.no_cache = 1

	# Get shop name from query parameter
	shop_name = frappe.form_dict.get("id")

	if not shop_name:
		frappe.throw(_("Shop ID is required"), frappe.DoesNotExistError)

	# Get shop details
	try:
		shop = frappe.get_doc("Shop", shop_name)
	except frappe.DoesNotExistError:
		frappe.throw(_("Shop {0} not found").format(shop_name))

	context.shop = shop
	context.title = shop.shop_name or shop.shop_number

	# Get airport details
	if shop.airport:
		context.airport_name = frappe.db.get_value("Airport", shop.airport, "name")

	# Get tenant details if shop is occupied
	if shop.tenant:
		context.tenant = frappe.get_doc("Tenant", shop.tenant)

	# Get active contract if exists
	if shop.tenant:
		contracts = frappe.get_all(
			"Rent Contract",
			filters={
				"shop": shop.name,
				"tenant": shop.tenant,
				"status": "Active"
			},
			fields=["name", "rent_amount", "start_date", "end_date"],
			limit=1
		)
		if contracts:
			context.contract = contracts[0]

	return context
