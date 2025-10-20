# Airport Management System

A comprehensive airport management application built with Frappe Framework v15. This app manages flights, tickets, crew, airport shops, tenant rentals, and provides a public web portal for shop leasing.

## 📋 Overview

The Airport Management System handles:
- ✈️ **Flight Management**: Airplanes, flights, crew scheduling, gate assignments
- 🎫 **Ticket Management**: Passenger bookings, seat assignments, add-ons
- 🏪 **Shop Management**: Airport retail spaces, tenant contracts, rent collection
- 📊 **Analytics**: Revenue reports, occupancy tracking, performance metrics
- 🌐 **Web Portal**: Public shop listings and lead capture
- 🔌 **REST API**: Complete CRUD operations for external integrations

## 🚀 Quick Start

### Prerequisites
- Frappe Framework v15
- MariaDB/PostgreSQL
- Python 3.10+
- Node.js 18+

### Installation

```bash
# Get the app
cd ~/frappe-bench
bench get-app airport

# Install on site
bench --site your-site-name install-app airport

# Migrate database
bench --site your-site-name migrate

# Build assets
bench --site your-site-name build

# Start development server
bench start
```

Visit: `http://localhost:8000`

### First Time Setup

1. **Load Sample Data** (Recommended)
   ```bash
   cd apps/airport
   ./load_sample_data.sh your-site-name
   ```
   This creates 80+ sample records for immediate testing.

2. **Or Create Data Manually:**
   - Add Airports
   - Add Airlines
   - Create Airplanes
   - Create Flights
   - Set up Shops and Tenants

3. **Verify Setup**
   - Check Shop Types exist (Stall, Walk-through, Normal)
   - Visit Airport Shop Settings
   - Browse to `/shops` to see web portal

## 📚 Documentation

- **Quick Start**: See `QUICK_START.md` for 5-minute setup guide
- **Implementation Details**: See `claude.md` for complete technical documentation
- **Day 4 Summary**: See `DAY_4_IMPLEMENTATION_SUMMARY.md`
- **API Documentation**: See `bruno_api_collection/README.md`

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/airport
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

## 🎯 Key Features

### Flight Management
- **Airplane Fleet**: Track aircraft, capacity, status
- **Flight Scheduling**: Route planning, crew assignment
- **Gate Management**: Automatic gate number updates across tickets
- **Background Jobs**: Async ticket updates when flight details change

### Ticket Management
- **Passenger Bookings**: Automated seat assignment
- **Add-ons**: Extra services and charges
- **Capacity Validation**: Prevents overbooking
- **Status Tracking**: Booked → Checked-In → Boarded

### Airport Shops Module
- **Shop Types**: Categorized retail spaces (Stall, Walk-through, Normal)
- **Tenant Management**: Contact info, contract tracking
- **Rent Contracts**: Automated rent reminders, payment tracking
- **Rent Receipts**: Professional print format
- **Occupancy Analytics**: Real-time availability tracking

### Web Portal (No Base Template)
- **Public Shop Listings**: Browse available spaces at `/shops`
- **Shop Details**: Comprehensive information at `/shop/<name>`
- **Lead Capture**: Express interest form at `/shop-lead`
- **Custom Styling**: Gradient design, fully responsive

### Reports & Analytics
- **Revenue by Airline**: Track airline-wise revenue
- **Shops by Airport**: Occupancy rates, total area
- **Add-on Popularity**: Best-selling services

### REST API
- Complete CRUD for Shop doctype
- Token-based authentication
- Bruno API collection included
- Comprehensive documentation

## 🏗️ Architecture

### DocTypes

**Airport Module:**
- Airline
- Airplane
- Airport
- Airplane Flight
- Airplane Ticket
- Flight Passenger
- Crew Members

**Airport Shops Module:**
- Shop
- Shop Type
- Tenant
- Rent Contract
- Rent Payment
- Shop Lead
- Airport Shop Settings (Single)

### Background Jobs
- Gate number synchronization across tickets
- Async processing for bulk updates
- Real-time user notifications

### Scheduler Events
- **Monthly**: Rent reminder emails to tenants
- Configurable via Airport Shop Settings
- HTML-formatted professional emails

### Web Pages
- `/shops` - Shop listing
- `/shop/<name>` - Shop details
- `/shop-lead` - Lead submission form
- `/flights` - Flight listings (WebsiteGenerator)

## 🔧 Technical Stack

- **Backend**: Python 3.10+, Frappe Framework v15
- **Frontend**: HTML5, JavaScript, Jinja2
- **Database**: MariaDB/PostgreSQL
- **Styling**: Custom CSS (400+ lines)
- **API**: REST with Token Authentication
- **Background Jobs**: `frappe.enqueue()`
- **Scheduler**: Cron-based (monthly)

## 📊 Database Schema Highlights

### Core Relationships
```
Airline ──< Airplane ──< Airplane Flight ──< Airplane Ticket >── Flight Passenger
                                     │
                                     └──< Crew Members

Airport ──< Shop ──< Rent Contract ──< Rent Payment
             │              │
             └─< Tenant ────┘
             │
             └─< Shop Type

Shop ──< Shop Lead
```

## 🔐 Security Features

- Role-based permissions (System Manager, Travel Agent, Fleet Manager, etc.)
- API token authentication
- CSRF protection in web forms
- Input validation and sanitization
- Permission checks in controllers

## 🧪 Testing

### Manual Testing
See `QUICK_START.md` for step-by-step testing guide.

### API Testing
Import Bruno collection from `bruno_api_collection/` and test all endpoints.

### Background Jobs
```bash
# Change gate number in any flight to trigger job
# Watch for blue notification
# Verify tickets updated
```

### Scheduler
```bash
bench --site localhost execute airport.airport_shops.doctype.rent_contract.rent_contract.send_monthly_rent_reminders
```

## 📖 API Documentation

### Generate API Keys
1. Login → User Menu → My Settings
2. API Access → Generate Keys
3. Copy Key and Secret

### Example Request
```bash
curl -X GET "http://localhost:8000/api/resource/Shop?fields=[\"*\"]" \
  -H "Authorization: token {api_key}:{api_secret}"
```

### Available Endpoints
- `GET /api/resource/Shop` - List shops
- `GET /api/resource/Shop/{name}` - Get shop
- `POST /api/resource/Shop` - Create shop
- `PUT /api/resource/Shop/{name}` - Update shop
- `DELETE /api/resource/Shop/{name}` - Delete shop

Full documentation: `bruno_api_collection/README.md`

## 🎓 Learning Resources

This app demonstrates:
- Frappe DocType development
- Background job processing
- Scheduler event configuration
- Fixtures for master data
- Client-side scripting (set_query)
- Web portal development
- Custom print formats
- Script report development
- REST API integration
- Email notifications

## 🤝 Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/airport
pre-commit install
```

Pre-commit is configured to use:
- ruff (Python linting)
- eslint (JavaScript linting)
- prettier (Code formatting)
- pyupgrade (Python syntax upgrades)

### Development Workflow
1. Create feature branch
2. Make changes
3. Run tests
4. Submit pull request

## 📝 License

apache-2.0

## 👥 Credits

Developed as part of Frappe Framework Certification Program - Day 4 Assignment

**Developer**: Claude Code AI Assistant
**Framework**: Frappe Framework v15
**Date**: October 2025

## 🆘 Support

For issues or questions:
1. Check documentation in `/docs` folder
2. Review `claude.md` for implementation details
3. Visit Frappe Forum: https://discuss.frappe.io
4. Check Frappe Docs: https://frappeframework.com/docs

## 🎉 Acknowledgments

Special thanks to the Frappe Framework team for creating an excellent low-code platform.
