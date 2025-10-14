# Copyright (c) 2025, Unity and contributors
# For license information, please see license.txt

import random
import frappe


def execute():
	"""
	Patch to populate the seat field for existing Airplane Ticket documents.
	This is needed because the seat field was added after some tickets were already created.
	The before_insert() hook only runs for NEW documents, not existing ones.
	"""

	# Get all Airplane Ticket documents
	tickets = frappe.get_all("Airplane Ticket", fields=["name", "seat"])

	# Counter for tracking updates
	updated_count = 0

	for ticket in tickets:
		# Only populate if seat is empty
		if not ticket.seat:
			# Generate random seat number (1-99) and letter (A-E)
			seat_number = random.randint(1, 99)
			seat_letter = random.choice(['A', 'B', 'C', 'D', 'E'])
			seat = f"{seat_number}{seat_letter}"

			# Update the seat field directly in database
			# Using db_set to avoid triggering validations and other hooks
			frappe.db.set_value("Airplane Ticket", ticket.name, "seat", seat)

			updated_count += 1

	# Commit the changes to database
	frappe.db.commit()

	# Print summary
	print(f"Patch completed: Updated {updated_count} out of {len(tickets)} Airplane Tickets with seat assignments")
