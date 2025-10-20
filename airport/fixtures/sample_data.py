"""
Sample data creation script for testing
Run with: bench --site localhost execute airport.fixtures.sample_data.create_sample_data
"""

import frappe
from frappe.utils import today, add_days, add_months, now_datetime


def create_sample_data():
	"""Create sample data for all DocTypes"""
	frappe.set_user("Administrator")

	print("Creating sample data for Airport Management System...")

	# Create in order of dependencies
	create_airlines()
	create_airports()
	create_airplanes()
	create_flight_passengers()
	create_addon_types()  # Create add-on types first
	create_airplane_flights()
	create_airplane_tickets()
	create_shop_types()  # Will use existing fixtures
	create_tenants()
	create_shops()
	create_rent_contracts()
	create_rent_payments()
	create_shop_leads()
	create_airport_shop_settings()

	frappe.db.commit()
	print("✅ Sample data creation complete!")


def create_airlines():
	"""Create or update 5 airlines"""
	airlines = [
		{"name": "Air India", "website": "https://airindia.com", "customer_care_number": "+91-22-1234-5678", "headquarters": "Mumbai", "founding_year": 1932},
		{"name": "IndiGo", "website": "https://goindigo.in", "customer_care_number": "+91-124-6173838", "headquarters": "Gurgaon", "founding_year": 2006},
		{"name": "SpiceJet", "website": "https://spicejet.com", "customer_care_number": "+91-987-1803333", "headquarters": "Gurgaon", "founding_year": 2005},
		{"name": "Vistara", "website": "https://airvistara.com", "customer_care_number": "+91-9289228888", "headquarters": "Gurgaon", "founding_year": 2015},
		{"name": "AirAsia India", "website": "https://airasia.com", "customer_care_number": "+91-80-46189000", "headquarters": "Bengaluru", "founding_year": 2014}
	]

	for data in airlines:
		try:
			if frappe.db.exists("Airline", data["name"]):
				# Update existing
				doc = frappe.get_doc("Airline", data["name"])
				doc.website = data["website"]
				doc.customer_care_number = data["customer_care_number"]
				doc.headquarters = data["headquarters"]
				doc.founding_year = data["founding_year"]
				doc.save(ignore_permissions=True)
				print(f"✓ Updated Airline: {data['name']}")
			else:
				# Create new
				doc = frappe.get_doc({
					"doctype": "Airline",
					"__newname": data["name"],
					"website": data["website"],
					"customer_care_number": data["customer_care_number"],
					"headquarters": data["headquarters"],
					"founding_year": data["founding_year"]
				})
				doc.insert(ignore_permissions=True)
				print(f"✓ Created Airline: {data['name']}")
		except Exception as e:
			print(f"⚠️ Error with Airline {data['name']}: {str(e)}")


def create_airports():
	"""Create or update 5 airports"""
	airports = [
		{"code": "DEL", "city": "New Delhi", "country": "India"},
		{"code": "BOM", "city": "Mumbai", "country": "India"},
		{"code": "BLR", "city": "Bangalore", "country": "India"},
		{"code": "HYD", "city": "Hyderabad", "country": "India"},
		{"code": "MAA", "city": "Chennai", "country": "India"}
	]

	for data in airports:
		try:
			if frappe.db.exists("Airport", data["code"]):
				# Update existing
				doc = frappe.get_doc("Airport", data["code"])
				doc.code = data["code"]
				doc.city = data["city"]
				doc.country = data["country"]
				doc.save(ignore_permissions=True)
				print(f"✓ Updated Airport: {data['code']} - {data['city']}, {data['country']}")
			else:
				# Create new
				doc = frappe.get_doc({
					"doctype": "Airport",
					"__newname": data["code"],
					"code": data["code"],
					"city": data["city"],
					"country": data["country"]
				})
				doc.insert(ignore_permissions=True)
				print(f"✓ Created Airport: {data['code']} - {data['city']}, {data['country']}")
		except Exception as e:
			print(f"⚠️ Error with Airport {data['code']}: {str(e)}")


def create_airplanes():
	"""Create 6 airplanes"""
	airlines = frappe.get_all("Airline", pluck="name")

	if len(airlines) < 5:
		print(f"⚠️ Need at least 5 airlines to create airplanes (found {len(airlines)})")
		return

	airplanes = [
		{"airline": airlines[0], "capacity": 180, "model": "Boeing 737"},
		{"airline": airlines[1], "capacity": 189, "model": "Airbus A320"},
		{"airline": airlines[2], "capacity": 186, "model": "Boeing 737-800"},
		{"airline": airlines[3], "capacity": 164, "model": "Airbus A320neo"},
		{"airline": airlines[4], "capacity": 220, "model": "Boeing 777"},
		{"airline": airlines[0], "capacity": 180, "model": "Boeing 737-MAX"}
	]

	for data in airplanes:
		try:
			doc = frappe.get_doc({
				"doctype": "Airplane",
				"airline": data["airline"],
				"capacity": data["capacity"],
				"model": data["model"]
			})
			doc.insert(ignore_permissions=True)
			print(f"✓ Created Airplane: {doc.name} - {data['model']}")
		except Exception as e:
			print(f"⚠️ Error creating airplane: {str(e)}")


def create_flight_passengers():
	"""Create or update 10 passengers"""
	passengers = [
		{"first_name": "Rajesh", "last_name": "Kumar", "email": "rajesh.kumar@example.com", "phone": "+91-9876543210", "date_of_birth": "1985-05-15"},
		{"first_name": "Priya", "last_name": "Sharma", "email": "priya.sharma@example.com", "phone": "+91-9876543211", "date_of_birth": "1990-08-22"},
		{"first_name": "Amit", "last_name": "Patel", "email": "amit.patel@example.com", "phone": "+91-9876543212", "date_of_birth": "1988-03-10"},
		{"first_name": "Sneha", "last_name": "Reddy", "email": "sneha.reddy@example.com", "phone": "+91-9876543213", "date_of_birth": "1992-11-30"},
		{"first_name": "Vikram", "last_name": "Singh", "email": "vikram.singh@example.com", "phone": "+91-9876543214", "date_of_birth": "1987-01-25"},
		{"first_name": "Anita", "last_name": "Desai", "email": "anita.desai@example.com", "phone": "+91-9876543215", "date_of_birth": "1995-07-18"},
		{"first_name": "Rohit", "last_name": "Mehta", "email": "rohit.mehta@example.com", "phone": "+91-9876543216", "date_of_birth": "1983-09-05"},
		{"first_name": "Kavya", "last_name": "Iyer", "email": "kavya.iyer@example.com", "phone": "+91-9876543217", "date_of_birth": "1991-12-14"},
		{"first_name": "Arjun", "last_name": "Nair", "email": "arjun.nair@example.com", "phone": "+91-9876543218", "date_of_birth": "1989-04-28"},
		{"first_name": "Divya", "last_name": "Chopra", "email": "divya.chopra@example.com", "phone": "+91-9876543219", "date_of_birth": "1993-06-20"}
	]

	for data in passengers:
		try:
			# Check for existing passenger using first_name, last_name, and date_of_birth
			existing = frappe.db.exists("Flight Passenger", {
				"first_name": data["first_name"],
				"last_name": data["last_name"],
				"date_of_birth": data["date_of_birth"]
			})

			if existing:
				# Update existing
				doc = frappe.get_doc("Flight Passenger", existing)
				doc.email = data["email"]
				doc.phone = data["phone"]
				doc.save(ignore_permissions=True)
				print(f"✓ Updated Passenger: {data['first_name']} {data['last_name']}")
			else:
				# Create new
				doc = frappe.get_doc({
					"doctype": "Flight Passenger",
					"first_name": data["first_name"],
					"last_name": data["last_name"],
					"email": data["email"],
					"phone": data["phone"],
					"date_of_birth": data["date_of_birth"]
				})
				doc.insert(ignore_permissions=True)
				print(f"✓ Created Passenger: {data['first_name']} {data['last_name']}")
		except Exception as e:
			print(f"⚠️ Error with passenger {data['first_name']}: {str(e)}")


def create_addon_types():
	"""Create or update airplane ticket add-on types"""
	addon_types = [
		{"name": "Extra Baggage", "description": "Additional 20kg baggage allowance"},
		{"name": "Priority Boarding", "description": "Board the plane first"},
		{"name": "In-Flight Meal", "description": "Premium meal service during flight"},
		{"name": "Extra Legroom", "description": "Seats with additional legroom"},
		{"name": "WiFi Access", "description": "Internet connectivity during flight"},
		{"name": "Travel Insurance", "description": "Comprehensive travel insurance coverage"}
	]

	for data in addon_types:
		try:
			if frappe.db.exists("Airplane Ticket Add-on Type", data["name"]):
				# Update existing
				doc = frappe.get_doc("Airplane Ticket Add-on Type", data["name"])
				doc.description = data["description"]
				doc.save(ignore_permissions=True)
				print(f"✓ Updated Add-on Type: {data['name']}")
			else:
				# Create new
				doc = frappe.get_doc({
					"doctype": "Airplane Ticket Add-on Type",
					"__newname": data["name"],
					"description": data["description"]
				})
				doc.insert(ignore_permissions=True)
				print(f"✓ Created Add-on Type: {data['name']}")
		except Exception as e:
			print(f"⚠️ Error with Add-on Type {data['name']}: {str(e)}")


def create_airplane_flights():
	"""Create 8 flights"""
	airplanes = frappe.get_all("Airplane", pluck="name")
	airports = frappe.get_all("Airport", pluck="name")

	if len(airplanes) < 3 or len(airports) < 5:
		print(f"⚠️ Need at least 3 airplanes and 5 airports to create flights (found {len(airplanes)} airplanes, {len(airports)} airports)")
		print("⚠️ Skipping flight creation - please ensure airplanes and airports are created first")
		return

	flights = [
		{"airplane": airplanes[0], "source": airports[0], "dest": airports[1], "date": today(), "time": "08:00:00", "duration": 7200, "gate": "A1"},
		{"airplane": airplanes[1], "source": airports[1], "dest": airports[2], "date": today(), "time": "10:30:00", "duration": 5400, "gate": "B2"},
		{"airplane": airplanes[2], "source": airports[2], "dest": airports[3], "date": add_days(today(), 1), "time": "14:00:00", "duration": 3600, "gate": "C3"},
		{"airplane": airplanes[0], "source": airports[3], "dest": airports[4], "date": add_days(today(), 1), "time": "16:45:00", "duration": 4500, "gate": "D4"},
		{"airplane": airplanes[1], "source": airports[4], "dest": airports[0], "date": add_days(today(), 2), "time": "18:30:00", "duration": 6300, "gate": "A5"},
		{"airplane": airplanes[2], "source": airports[0], "dest": airports[3], "date": add_days(today(), 2), "time": "09:15:00", "duration": 6900, "gate": "B1"},
		{"airplane": airplanes[0], "source": airports[2], "dest": airports[0], "date": add_days(today(), 3), "time": "11:00:00", "duration": 7200, "gate": "C2"},
		{"airplane": airplanes[1], "source": airports[1], "dest": airports[4], "date": add_days(today(), 3), "time": "15:30:00", "duration": 5100, "gate": "D3"}
	]

	for data in flights:
		try:
			doc = frappe.get_doc({
				"doctype": "Airplane Flight",
				"airplane": data["airplane"],
				"source_airport": data["source"],
				"destination_airport": data["dest"],
				"date_of_departure": data["date"],
				"time_of_departure": data["time"],
				"duration": data["duration"],
				"gate_number": data["gate"],
				"status": "Scheduled"
			})
			doc.insert(ignore_permissions=True)
			print(f"Created Flight: {data['airplane']} from {data['source']} to {data['dest']}")
		except Exception as e:
			print(f"⚠️ Error creating flight: {str(e)}")


def create_airplane_tickets():
	"""Create tickets for flights with add-ons for some tickets"""
	flights = frappe.get_all("Airplane Flight", fields=["name"], limit=5)
	passengers = frappe.get_all("Flight Passenger", pluck="name")
	addon_types = frappe.get_all("Airplane Ticket Add-on Type", pluck="name")

	if not flights or not passengers:
		print("⚠️ Need flights and passengers to create tickets")
		return

	# Define add-on combinations (some tickets will have these, some won't)
	addon_combinations = [
		[{"item": "Extra Baggage", "amount": 1500}, {"item": "In-Flight Meal", "amount": 800}],
		[{"item": "Priority Boarding", "amount": 1000}],
		[{"item": "Extra Legroom", "amount": 2000}, {"item": "WiFi Access", "amount": 500}],
		[{"item": "Travel Insurance", "amount": 1200}],
		[]  # No add-ons
	]

	ticket_count = 0
	for i, flight in enumerate(flights):
		# Create 2-3 tickets per flight
		num_tickets = 2 if i % 2 == 0 else 3
		for j in range(num_tickets):
			try:
				passenger_idx = (i * 3 + j) % len(passengers)

				# Determine if this ticket should have add-ons (60% chance)
				has_addons = (i + j) % 5 != 4  # Skip every 5th ticket for variety

				doc = frappe.get_doc({
					"doctype": "Airplane Ticket",
					"flight": flight.name,
					"passenger": passengers[passenger_idx],
					"flight_price": 5000 + (i * 500),
					"status": "Booked"
				})

				# Add add-ons to some tickets (not all)
				if has_addons and addon_types:
					addon_set = addon_combinations[(i + j) % len(addon_combinations)]
					if addon_set:  # Only if this combination has add-ons
						for addon in addon_set:
							if addon["item"] in addon_types:
								doc.append("add_ons", {
									"item": addon["item"],
									"amount": addon["amount"]
								})

				doc.insert(ignore_permissions=True)

				addon_info = f" (with {len(doc.add_ons)} add-ons)" if doc.add_ons else ""
				print(f"✓ Created Ticket: {doc.name}{addon_info}")
				ticket_count += 1
			except Exception as e:
				print(f"⚠️ Error creating ticket: {str(e)}")

	print(f"Total: {ticket_count} Airplane Tickets created")


def create_shop_types():
	"""Shop types are created via fixtures, just verify"""
	shop_types = frappe.get_all("Shop Type", pluck="name")
	if shop_types:
		print(f"✓ Shop Types already exist: {', '.join(shop_types)}")
	else:
		# Create manually if fixtures haven't run
		types = ["Stall", "Walk-through", "Normal"]
		for type_name in types:
			if not frappe.db.exists("Shop Type", type_name):
				doc = frappe.get_doc({
					"doctype": "Shop Type",
					"type_name": type_name,
					"enabled": 1
				})
				doc.insert()
				print(f"Created Shop Type: {type_name}")


def create_tenants():
	"""Create or update 8 tenants"""
	tenants = [
		{"name": "Coffee Beans Inc", "contact": "Ramesh Kumar", "email": "ramesh@coffeebeans.com", "phone": "+91-9800000001", "company": "Coffee Beans Inc", "address": "123 MG Road, Mumbai, Maharashtra 400001"},
		{"name": "Book Haven", "contact": "Sita Patel", "email": "sita@bookhaven.com", "phone": "+91-9800000002", "company": "Book Haven Pvt Ltd", "address": "45 Park Street, Kolkata, West Bengal 700016"},
		{"name": "Tech Gadgets", "contact": "Vijay Reddy", "email": "vijay@techgadgets.com", "phone": "+91-9800000003", "company": "Tech Gadgets India", "address": "78 Brigade Road, Bangalore, Karnataka 560001"},
		{"name": "Fashion Hub", "contact": "Meera Shah", "email": "meera@fashionhub.com", "phone": "+91-9800000004", "company": "Fashion Hub Ltd", "address": "56 Connaught Place, New Delhi, Delhi 110001"},
		{"name": "Healthy Bites", "contact": "Arun Nair", "email": "arun@healthybites.com", "phone": "+91-9800000005", "company": "Healthy Bites", "address": "34 Anna Salai, Chennai, Tamil Nadu 600002"},
		{"name": "Travel Essentials", "contact": "Lakshmi Iyer", "email": "lakshmi@travelessentials.com", "phone": "+91-9800000006", "company": "Travel Essentials", "address": "89 Commercial Street, Bangalore, Karnataka 560001"},
		{"name": "Quick Snacks", "contact": "Karthik Menon", "email": "karthik@quicksnacks.com", "phone": "+91-9800000007", "company": "Quick Snacks Co", "address": "12 Marine Drive, Mumbai, Maharashtra 400002"},
		{"name": "Gift Gallery", "contact": "Pooja Sharma", "email": "pooja@giftgallery.com", "phone": "+91-9800000008", "company": "Gift Gallery", "address": "67 Banjara Hills, Hyderabad, Telangana 500034"}
	]

	for data in tenants:
		try:
			existing = frappe.db.exists("Tenant", {"email": data["email"]})
			if existing:
				# Update existing
				doc = frappe.get_doc("Tenant", existing)
				doc.tenant_name = data["name"]
				doc.contact_person = data["contact"]
				doc.phone_number = data["phone"]
				doc.company_name = data["company"]
				doc.address = data["address"]
				doc.save(ignore_permissions=True)
				print(f"✓ Updated Tenant: {data['name']}")
			else:
				# Create new
				doc = frappe.get_doc({
					"doctype": "Tenant",
					"tenant_name": data["name"],
					"contact_person": data["contact"],
					"email": data["email"],
					"phone_number": data["phone"],
					"company_name": data["company"],
					"address": data["address"]
				})
				doc.insert(ignore_permissions=True)
				print(f"✓ Created Tenant: {data['name']}")
		except Exception as e:
			print(f"⚠️ Error with tenant {data['name']}: {str(e)}")


def create_shops():
	"""Create 12 shops across airports"""
	airports = frappe.get_all("Airport", pluck="name")
	shop_types = frappe.get_all("Shop Type", pluck="name")
	tenants = frappe.get_all("Tenant", pluck="name")

	if not airports:
		print("⚠️ Need airports to create shops")
		return

	shops = [
		{"number": "S101", "name": "Coffee Corner", "type": shop_types[0] if shop_types else None, "area": 150, "status": "Occupied", "airport": airports[0], "tenant": tenants[0] if tenants else None},
		{"number": "S102", "name": "Book Store", "type": shop_types[2] if len(shop_types) > 2 else None, "area": 300, "status": "Occupied", "airport": airports[0], "tenant": tenants[1] if len(tenants) > 1 else None},
		{"number": "S103", "name": "Electronics Hub", "type": shop_types[2] if len(shop_types) > 2 else None, "area": 250, "status": "Occupied", "airport": airports[0], "tenant": tenants[2] if len(tenants) > 2 else None},
		{"number": "S104", "name": "Fashion Outlet", "type": shop_types[1] if len(shop_types) > 1 else None, "area": 400, "status": "Available", "airport": airports[0], "tenant": None},

		{"number": "S201", "name": "Juice Bar", "type": shop_types[0] if shop_types else None, "area": 120, "status": "Occupied", "airport": airports[1] if len(airports) > 1 else airports[0], "tenant": tenants[4] if len(tenants) > 4 else None},
		{"number": "S202", "name": "Travel Shop", "type": shop_types[2] if len(shop_types) > 2 else None, "area": 280, "status": "Occupied", "airport": airports[1] if len(airports) > 1 else airports[0], "tenant": tenants[5] if len(tenants) > 5 else None},
		{"number": "S203", "name": "Snack Zone", "type": shop_types[0] if shop_types else None, "area": 180, "status": "Available", "airport": airports[1] if len(airports) > 1 else airports[0], "tenant": None},

		{"number": "S301", "name": "Gift Shop", "type": shop_types[2] if len(shop_types) > 2 else None, "area": 220, "status": "Occupied", "airport": airports[2] if len(airports) > 2 else airports[0], "tenant": tenants[7] if len(tenants) > 7 else None},
		{"number": "S302", "name": "Premium Lounge Shop", "type": shop_types[1] if len(shop_types) > 1 else None, "area": 350, "status": "Available", "airport": airports[2] if len(airports) > 2 else airports[0], "tenant": None},

		{"number": "S401", "name": "Duty Free", "type": shop_types[2] if len(shop_types) > 2 else None, "area": 500, "status": "Available", "airport": airports[3] if len(airports) > 3 else airports[0], "tenant": None},
		{"number": "S402", "name": "Quick Bites", "type": shop_types[0] if shop_types else None, "area": 140, "status": "Occupied", "airport": airports[3] if len(airports) > 3 else airports[0], "tenant": tenants[6] if len(tenants) > 6 else None},

		{"number": "S501", "name": "Boutique", "type": shop_types[2] if len(shop_types) > 2 else None, "area": 320, "status": "Available", "airport": airports[4] if len(airports) > 4 else airports[0], "tenant": None}
	]

	for data in shops:
		try:
			existing = frappe.db.exists("Shop", {"shop_number": data["number"]})
			if existing:
				# Update existing
				doc = frappe.get_doc("Shop", existing)
				doc.shop_name = data["name"]
				doc.shop_type = data["type"]
				doc.area = data["area"]
				doc.status = data["status"]
				doc.airport = data["airport"]
				doc.tenant = data["tenant"]
				doc.save(ignore_permissions=True)
				tenant_info = f" (Tenant: {data['tenant']})" if data['tenant'] else ""
				print(f"✓ Updated Shop: {data['number']} - {data['name']}{tenant_info}")
			else:
				# Create new
				doc = frappe.get_doc({
					"doctype": "Shop",
					"shop_number": data["number"],
					"shop_name": data["name"],
					"shop_type": data["type"],
					"area": data["area"],
					"status": data["status"],
					"airport": data["airport"],
					"tenant": data["tenant"]
				})
				doc.insert(ignore_permissions=True)
				tenant_info = f" (Tenant: {data['tenant']})" if data['tenant'] else ""
				print(f"✓ Created Shop: {data['number']} - {data['name']}{tenant_info}")
		except Exception as e:
			print(f"⚠️ Error with shop {data['number']}: {str(e)}")


def create_rent_contracts():
	"""Create or update contracts for occupied shops"""
	shops = frappe.get_all("Shop", filters={"status": "Occupied"}, fields=["name", "tenant"])

	contract_num = 1
	for shop in shops:
		if shop.tenant:
			try:
				# Check if contract already exists for this shop
				existing = frappe.db.exists("Rent Contract", {"shop": shop.name})

				if existing:
					# Update existing contract
					doc = frappe.get_doc("Rent Contract", existing)
					doc.tenant = shop.tenant
					doc.rent_amount = 10000 + (contract_num * 1000)
					doc.start_date = add_months(today(), -6)
					doc.end_date = add_months(today(), 6)
					doc.status = "Active"
					doc.save(ignore_permissions=True)
					print(f"✓ Updated Rent Contract: {doc.name}")
				else:
					# Create new contract
					doc = frappe.get_doc({
						"doctype": "Rent Contract",
						"contract_number": f"RC-2025-{contract_num:04d}",
						"shop": shop.name,
						"tenant": shop.tenant,
						"rent_amount": 10000 + (contract_num * 1000),
						"start_date": add_months(today(), -6),
						"end_date": add_months(today(), 6),
						"status": "Active"
					})
					doc.insert(ignore_permissions=True)
					print(f"✓ Created Rent Contract: {doc.name}")
				contract_num += 1
			except Exception as e:
				print(f"⚠️ Error with contract for shop {shop.name}: {str(e)}")


def create_rent_payments():
	"""Create rent payments for contracts"""
	contracts = frappe.get_all("Rent Contract", fields=["name", "shop", "tenant", "rent_amount"], limit=5)

	payment_methods = ["Bank Transfer", "Cheque", "UPI", "Cash"]

	payment_count = 0
	for i, contract in enumerate(contracts):
		# Create 2 payments per contract
		for j in range(2):
			try:
				doc = frappe.get_doc({
					"doctype": "Rent Payment",
					"contract": contract.name,
					"shop": contract.shop,
					"tenant": contract.tenant,
					"amount": contract.rent_amount,
					"payment_method": payment_methods[i % len(payment_methods)],
					"payment_date": add_months(today(), -(j+1)),
					"status": "Paid"
				})
				doc.insert(ignore_permissions=True)
				payment_count += 1
			except Exception as e:
				print(f"⚠️ Error creating payment: {str(e)}")

	print(f"Created {payment_count} Rent Payments")


def create_shop_leads():
	"""Create shop leads"""
	shops = frappe.get_all("Shop", filters={"status": "Available"}, pluck="name", limit=5)

	leads = [
		{"name": "Mohan Gupta", "email": "mohan.gupta@example.com", "phone": "+91-9700000001", "company": "Gupta Enterprises"},
		{"name": "Sunita Verma", "email": "sunita.verma@example.com", "phone": "+91-9700000002", "company": "Verma Trading"},
		{"name": "Rajiv Malhotra", "email": "rajiv.malhotra@example.com", "phone": "+91-9700000003", "company": "Malhotra Retail"},
		{"name": "Anjali Khanna", "email": "anjali.khanna@example.com", "phone": "+91-9700000004", "company": "Khanna Foods"},
		{"name": "Deepak Rao", "email": "deepak.rao@example.com", "phone": "+91-9700000005", "company": "Rao Stores"}
	]

	for i, lead_data in enumerate(leads):
		if i < len(shops):
			try:
				existing = frappe.db.exists("Shop Lead", {"email": lead_data["email"]})
				if existing:
					# Update existing
					doc = frappe.get_doc("Shop Lead", existing)
					doc.full_name = lead_data["name"]
					doc.phone = lead_data["phone"]
					doc.company_name = lead_data["company"]
					doc.shop_interest = shops[i]
					doc.message = f"Interested in leasing {shops[i]} for retail business."
					doc.save(ignore_permissions=True)
					print(f"✓ Updated Shop Lead: {lead_data['name']}")
				else:
					# Create new
					doc = frappe.get_doc({
						"doctype": "Shop Lead",
						"full_name": lead_data["name"],
						"email": lead_data["email"],
						"phone": lead_data["phone"],
						"company_name": lead_data["company"],
						"shop_interest": shops[i],
						"message": f"Interested in leasing {shops[i]} for retail business.",
						"status": "New",
						"lead_date": today()
					})
					doc.insert(ignore_permissions=True)
					print(f"✓ Created Shop Lead: {lead_data['name']}")
			except Exception as e:
				print(f"⚠️ Error with lead {lead_data['name']}: {str(e)}")


def create_airport_shop_settings():
	"""Create or update Airport Shop Settings"""
	if frappe.db.exists("Airport Shop Settings", "Airport Shop Settings"):
		doc = frappe.get_doc("Airport Shop Settings", "Airport Shop Settings")
		print("✓ Airport Shop Settings already exists")
	else:
		doc = frappe.get_doc({
			"doctype": "Airport Shop Settings",
			"default_rent_amount": 15000,
			"enable_rent_reminders": 1
		})
		doc.insert()
		print("Created Airport Shop Settings")

	# Update values
	doc.default_rent_amount = 15000
	doc.enable_rent_reminders = 1
	doc.save()
	print("Updated Airport Shop Settings: Default Rent = 15000, Reminders = Enabled")


if __name__ == "__main__":
	create_sample_data()
