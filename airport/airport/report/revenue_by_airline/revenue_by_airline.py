# Copyright (c) 2025, Unity and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data()
	chart = get_chart_data(data)
	summary = get_summary(data)
	return columns, data, None, chart, summary

def get_columns():
	return [
		{
			"fieldname": "airline",
			"label": _("Airline"),
			"fieldtype": "Link",
			"options": "Airline",
			"width": 200
		},
		{
			"fieldname": "revenue",
			"label": _("Revenue"),
			"fieldtype": "Currency",
			"width": 200
		}
	]

def get_data():
	airlines = frappe.get_all("Airline", fields=["name"])
	data = []
	for airline in airlines:
		airplanes = frappe.get_all("Airplane", fields=["name"], filters={"airline": airline.name})
		airplane_names = [airplane.name for airplane in airplanes]
		if airplane_names:
			flights = frappe.get_all("Airplane Flight", fields=["name"], filters={"airplane": ["in", airplane_names]})
			flight_names = [flight.name for flight in flights]

			if flight_names:
				tickets = frappe.get_all("Airplane Ticket", fields=["total_amount"], filters={"flight": ["in", flight_names], "docstatus": 1})
			
				revenue = sum([ticket.total_amount or 0 for ticket in tickets])
			else:
				revenue = 0
		else:
			revenue = 0
		data.append({
			"airline": airline.name,
			"revenue": revenue
		})
	return data

def get_chart_data(data):
	labels = [row["airline"] for row in data]
	values = [row["revenue"] for row in data]

	return {
		"data": {
			"labels": labels,
			"datasets": [
				{
					"name": "Revenue",
					"values": values
				}
			]
		},
		"type": "donut",
		"height": 300
	}


def get_summary(data):
	total_revenue = sum([row["revenue"] for row in data])

	return [
		{
			"value": total_revenue,
			"indicator": "Green",
			"label": "Total Revenue",
			"datatype": "Currency"
		}
	]