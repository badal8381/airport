# Copyright (c) 2025, Unity and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	"""
	Script Report to show shop statistics grouped by airport
	Shows total shops, available shops, occupied shops, and occupancy percentage
	"""
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	"""Define report columns"""
	return [
		{
			"fieldname": "airport",
			"label": _("Airport"),
			"fieldtype": "Link",
			"options": "Airport",
			"width": 200
		},
		{
			"fieldname": "total_shops",
			"label": _("Total Shops"),
			"fieldtype": "Int",
			"width": 120
		},
		{
			"fieldname": "available_shops",
			"label": _("Available"),
			"fieldtype": "Int",
			"width": 120
		},
		{
			"fieldname": "occupied_shops",
			"label": _("Occupied"),
			"fieldtype": "Int",
			"width": 120
		},
		{
			"fieldname": "occupancy_percentage",
			"label": _("Occupancy %"),
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"fieldname": "total_area",
			"label": _("Total Area (sq ft)"),
			"fieldtype": "Float",
			"width": 150
		}
	]


def get_data(filters):
	"""
	Fetch shop data grouped by airport
	"""
	conditions = ""
	if filters and filters.get("airport"):
		conditions = f"WHERE s.airport = '{filters.get('airport')}'"

	query = f"""
		SELECT
			s.airport,
			COUNT(s.name) as total_shops,
			SUM(CASE WHEN s.status = 'Available' THEN 1 ELSE 0 END) as available_shops,
			SUM(CASE WHEN s.status = 'Occupied' THEN 1 ELSE 0 END) as occupied_shops,
			CASE
				WHEN COUNT(s.name) > 0 THEN
					(SUM(CASE WHEN s.status = 'Occupied' THEN 1 ELSE 0 END) * 100.0 / COUNT(s.name))
				ELSE 0
			END as occupancy_percentage,
			SUM(s.area) as total_area
		FROM `tabShop` s
		{conditions}
		GROUP BY s.airport
		ORDER BY s.airport
	"""

	data = frappe.db.sql(query, as_dict=True)

	return data
