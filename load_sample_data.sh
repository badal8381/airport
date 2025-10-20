#!/bin/bash

# Load Sample Data Script
# This script loads sample data into the Airport Management System

echo "=========================================="
echo "Airport Management System - Sample Data Loader"
echo "=========================================="
echo ""

# Check if site name is provided
SITE_NAME=${1:-localhost}

echo "Site: $SITE_NAME"
echo ""

# Check if bench command exists
if ! command -v bench &> /dev/null; then
    echo "❌ Error: bench command not found"
    echo "Please run this script from the frappe-bench directory"
    exit 1
fi

echo "📊 Step 1: Creating sample data..."
echo "(Shop Type fixtures already loaded during migration)"
echo "This will create:"
echo "  - 5 Airlines"
echo "  - 5 Airports"
echo "  - 6 Airplanes"
echo "  - 10 Flight Passengers"
echo "  - 6 Ticket Add-on Types"
echo "  - 8 Airplane Flights"
echo "  - 15+ Airplane Tickets (some with add-ons, some without)"
echo "  - 3 Shop Types (via fixtures)"
echo "  - 8 Tenants"
echo "  - 12 Shops (across 5 airports)"
echo "  - 7+ Rent Contracts"
echo "  - 10+ Rent Payments"
echo "  - 5 Shop Leads"
echo "  - Airport Shop Settings"
echo ""

bench --site $SITE_NAME execute airport.fixtures.sample_data.create_sample_data

echo ""
echo "=========================================="
echo "✅ Sample data loaded successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Login to your site: http://localhost:8000"
echo "2. Explore the data:"
echo "   - Desk → Airplane Flight (8 flights)"
echo "   - Desk → Shop (12 shops)"
echo "   - Reports → Shops by Airport"
echo "   - Web Portal → http://localhost:8000/shops"
echo ""
echo "3. Test features:"
echo "   - Change gate number in a flight (triggers background job)"
echo "   - View rent receipts (Print → Rent Receipt)"
echo "   - Test REST API (see bruno_api_collection/)"
echo ""
