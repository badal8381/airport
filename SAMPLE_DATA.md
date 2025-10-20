# Sample Data Guide

## 📊 Overview

The Airport Management System includes a comprehensive sample data generator that creates realistic test data for all DocTypes.

## 🎯 What Gets Created

### Flight Operations (38+ records)
- **5 Airlines**: Air India, IndiGo, SpiceJet, Vistara, Emirates
- **5 Airports**: DEL, BOM, BLR, HYD, MAA
- **6 Airplanes**: Various aircraft with different capacities (164-220 seats)
- **10 Flight Passengers**: Indian names with contact details
- **8 Airplane Flights**: Scheduled over the next 3 days
- **15+ Airplane Tickets**: Distributed across flights

### Shop Management (40+ records)
- **3 Shop Types**: Stall, Walk-through, Normal (from fixtures)
- **8 Tenants**: Companies with contact persons
- **12 Shops**:
  - 4 shops at DEL (Delhi)
  - 3 shops at BOM (Mumbai)
  - 2 shops at BLR (Bangalore)
  - 2 shops at HYD (Hyderabad)
  - 1 shop at MAA (Chennai)
- **7+ Rent Contracts**: Active contracts for occupied shops
- **10+ Rent Payments**: Historical payment records
- **5 Shop Leads**: Prospective tenant inquiries
- **Airport Shop Settings**: Default rent = ₹15,000, Reminders enabled

## 🚀 Quick Load (Recommended)

### Method 1: Using the Shell Script

```bash
cd /home/badal/frappe-v15/apps/airport
./load_sample_data.sh localhost
```

This will:
1. Import fixtures
2. Create all sample data
3. Show summary of what was created

### Method 2: Manual Command

```bash
cd /home/badal/frappe-v15
bench --site localhost execute airport.fixtures.sample_data.create_sample_data
```

## 📋 Detailed Sample Data

### Airlines
| Name | Country | Website |
|------|---------|---------|
| Air India | India | airindia.com |
| IndiGo | India | goindigo.in |
| SpiceJet | India | spicejet.com |
| Vistara | India | airvistara.com |
| Emirates | UAE | emirates.com |

### Airports
| Code | City | Country |
|------|------|---------|
| DEL | Delhi | India |
| BOM | Mumbai | India |
| BLR | Bangalore | India |
| HYD | Hyderabad | India |
| MAA | Chennai | India |

### Sample Shops Distribution

**Delhi (DEL) - 4 shops:**
- S101: Coffee Corner (Stall, 150 sq ft) - Occupied
- S102: Book Store (Normal, 300 sq ft) - Occupied
- S103: Electronics Hub (Normal, 250 sq ft) - Occupied
- S104: Fashion Outlet (Walk-through, 400 sq ft) - Available

**Mumbai (BOM) - 3 shops:**
- S201: Juice Bar (Stall, 120 sq ft) - Occupied
- S202: Travel Shop (Normal, 280 sq ft) - Occupied
- S203: Snack Zone (Stall, 180 sq ft) - Available

**Bangalore (BLR) - 2 shops:**
- S301: Gift Shop (Normal, 220 sq ft) - Occupied
- S302: Premium Lounge Shop (Walk-through, 350 sq ft) - Available

**Hyderabad (HYD) - 2 shops:**
- S401: Duty Free (Normal, 500 sq ft) - Available
- S402: Quick Bites (Stall, 140 sq ft) - Occupied

**Chennai (MAA) - 1 shop:**
- S501: Boutique (Normal, 320 sq ft) - Available

### Sample Tenants
1. Coffee Beans Inc (Coffee Corner at DEL)
2. Book Haven (Book Store at DEL)
3. Tech Gadgets (Electronics Hub at DEL)
4. Healthy Bites (Juice Bar at BOM)
5. Travel Essentials (Travel Shop at BOM)
6. Quick Snacks (Quick Bites at HYD)
7. Gift Gallery (Gift Shop at BLR)

## 🧪 Testing Scenarios

### 1. Test Shop Occupancy Report
```
Desk → Reports → Shops by Airport
```
**Expected Results:**
- DEL: 4 shops (3 occupied, 1 available) = 75% occupancy
- BOM: 3 shops (2 occupied, 1 available) = 67% occupancy
- BLR: 2 shops (1 occupied, 1 available) = 50% occupancy
- HYD: 2 shops (1 occupied, 1 available) = 50% occupancy
- MAA: 1 shop (0 occupied, 1 available) = 0% occupancy

### 2. Test Background Job (Gate Number Update)
```
1. Open any Airplane Flight
2. Change gate number (e.g., A1 → A2)
3. Watch for blue notification
4. Open related tickets
5. Verify gate numbers updated
```

### 3. Test Web Portal
```
1. Visit: http://localhost:8000/shops
2. Should see 12 shop cards
3. Click on any shop to see details
4. Click "Express Interest" on available shops
5. Submit lead form
```

### 4. Test Rent Receipt Print
```
1. Open any Rent Payment record
2. Click Print button
3. Select "Rent Receipt" format
4. Verify professional layout displays
```

### 5. Test REST API
```bash
# Get all shops
curl -X GET "http://localhost:8000/api/resource/Shop?fields=[\"shop_number\",\"shop_name\",\"status\",\"airport\"]" \
  -H "Authorization: token YOUR_KEY:YOUR_SECRET"

# Should return 12 shops
```

## 🔄 Reset Sample Data

To clear and reload sample data:

```bash
# Method 1: Delete and recreate
bench --site localhost execute "frappe.delete_doc('Shop', frappe.get_all('Shop', pluck='name'), force=1)"
bench --site localhost execute airport.fixtures.sample_data.create_sample_data

# Method 2: Reinstall app (CAUTION: Clears all data)
bench --site localhost uninstall-app airport
bench --site localhost install-app airport
./load_sample_data.sh localhost
```

## 📊 Data Statistics

After loading sample data:

| DocType | Count |
|---------|-------|
| Airline | 5 |
| Airport | 5 |
| Airplane | 6 |
| Flight Passenger | 10 |
| Airplane Flight | 8 |
| Airplane Ticket | 15+ |
| Shop Type | 3 |
| Tenant | 8 |
| Shop | 12 |
| Rent Contract | 7+ |
| Rent Payment | 10+ |
| Shop Lead | 5 |
| **Total** | **80+** |

## 🎯 Use Cases Covered

### Flight Operations
✅ Multiple airlines operating flights
✅ Domestic routes across major Indian cities
✅ Scheduled flights over multiple days
✅ Passenger bookings with seat assignments
✅ Different aircraft types and capacities

### Shop Management
✅ Different shop types (Stall, Walk-through, Normal)
✅ Shops distributed across multiple airports
✅ Mix of occupied and available shops
✅ Active rental contracts with payment history
✅ Prospective tenant leads
✅ Various payment methods tracked

### Reports & Analytics
✅ Occupancy calculations per airport
✅ Revenue tracking from rent payments
✅ Lead pipeline for available shops

## 💡 Tips

1. **Realistic Dates**: Flights are scheduled for today and the next 3 days
2. **Payment History**: Each occupied shop has 2 historical payments
3. **Contact Details**: All emails and phones use example domains
4. **Customization**: Edit `airport/fixtures/sample_data.py` to customize data
5. **Incremental**: Running the script multiple times is safe (checks for existing records)

## 🐛 Troubleshooting

### "Need airplanes to create flights"
Run migration first: `bench --site localhost migrate`

### "Shop Types not found"
Import fixtures: `bench --site localhost import-fixtures`

### Data looks incomplete
Check error messages in the script output. Some data depends on other data being created first.

### Want fresh start
```bash
# Clear specific DocType
bench --site localhost console
>>> frappe.db.sql("DELETE FROM `tabShop`")
>>> frappe.db.commit()
```

## 📖 Related Documentation

- **Implementation Guide**: `claude.md`
- **Quick Start**: `QUICK_START.md`
- **API Testing**: `bruno_api_collection/README.md`
- **Full Documentation**: `README.md`

---

**Created**: 2025-10-20
**Purpose**: Testing and demonstration
**Data Type**: Fictional sample data for testing
