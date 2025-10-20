import frappe


def get_context(context):
	"""
	Get context for shops list page
	"""
	context.no_cache = 1

	# Get all shops
	shops = frappe.get_all(
		"Shop",
		fields=["name", "shop_number", "shop_name", "shop_type", "status", "area", "airport"],
		order_by="airport, shop_number"
	)

	# Get airport names for display
	for shop in shops:
		if shop.airport:
			shop.airport_name = frappe.db.get_value("Airport", shop.airport, "name")

	context.shops = shops
	context.title = "Airport Shops"

	return context
