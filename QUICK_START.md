# Quick Start Guide - Day 4 Implementation

## 🚀 Getting Started (5 Minutes)

### Step 1: Migrate Database
```bash
cd /home/badal/frappe-v15
bench --site localhost migrate
```
✅ Creates new DocTypes and loads fixtures

### Step 2: Build Assets
```bash
bench --site localhost build
```
✅ Compiles JavaScript and CSS

### Step 3: Clear Cache & Restart
```bash
bench --site localhost clear-cache
bench restart
```
✅ Refreshes the system

### Step 4: Load Sample Data (Recommended)
```bash
cd /home/badal/frappe-v15/apps/airport
./load_sample_data.sh localhost
```
✅ Creates 80+ sample records for testing

**What gets created:**
- 5 Airlines, 5 Airports, 6 Airplanes
- 10 Passengers, 8 Flights, 15+ Tickets
- 8 Tenants, 12 Shops, 7+ Contracts, 10+ Payments
- 5 Shop Leads

See `SAMPLE_DATA.md` for complete details.

---

## 🧪 Quick Tests (10 Minutes)

### 1. Check Shop Types (30 seconds)
```
Login → Desk → Search "Shop Type"
```
Should see: Stall, Walk-through, Normal (all enabled)

### 2. Configure Settings (1 minute)
```
Desk → Search "Airport Shop Settings"
Set default rent: 10000
Enable rent reminders: ✓
```

### 3. Test Background Job (2 minutes)
```
Open: Airplane Flight (any)
Change: Gate Number (e.g., A1 → A2)
Watch: Blue notification appears
Verify: Related tickets updated
```

### 4. Visit Web Portal (2 minutes)
```
Browser → http://localhost:8000/shops
Click: Any shop card
Click: "Express Interest"
Fill: Sample lead form
Submit: Check Shop Lead created in Desk
```

### 5. Test REST API (5 minutes)

#### Generate API Keys:
```
Desk → User Menu → My Settings → API Access → Generate Keys
Copy: API Key & Secret
```

#### Test with cURL:
```bash
# Replace YOUR_KEY and YOUR_SECRET
curl -X GET "http://localhost:8000/api/resource/Shop?fields=[\"*\"]" \
  -H "Authorization: token YOUR_KEY:YOUR_SECRET"
```

**Or use Bruno:**
1. Download from https://www.usebruno.com/
2. Open `apps/airport/bruno_api_collection/`
3. Update credentials in `environments/Local.bru`
4. Run GET All Shops request

---

## 📋 Feature Checklist

### Background Jobs
- [ ] Gate number changes trigger background job
- [ ] Tickets auto-update
- [ ] User sees notification

### Web Portal
- [ ] `/shops` loads shop list
- [ ] Shop cards display correctly
- [ ] Click shop → detail page works
- [ ] Lead form submits successfully

### Settings & Fixtures
- [ ] 3 shop types exist
- [ ] Shop form filters shop types
- [ ] Default rent applies to contracts

### Scheduler
```bash
# Manual test
bench --site localhost execute airport.airport_shops.doctype.rent_contract.rent_contract.send_monthly_rent_reminders
```
- [ ] Function runs without errors
- [ ] Check email queue (if active contracts exist)

### Print Format
- [ ] Create a Rent Payment
- [ ] Click Print → Rent Receipt
- [ ] Professional layout displays

### Reports
- [ ] Desk → Reports → Shops by Airport
- [ ] Data loads correctly
- [ ] Occupancy % calculates

---

## 🎯 What Each Feature Does

### 1. Gate Number Background Job
**What**: When you change a flight's gate number, all tickets update automatically
**Why**: Passengers need current gate information
**How**: Runs in background so UI doesn't freeze

### 2. Shop Type Fixtures
**What**: Pre-loaded shop categories (Stall, Walk-through, Normal)
**Why**: Standardized shop classification
**How**: Loaded during migration via hooks.py

### 3. Airport Shop Settings
**What**: Single global settings page
**Why**: Configure default rent & email reminders
**How**: Single DocType accessible from Desk

### 4. Rent Reminders
**What**: Monthly automated emails to tenants
**Why**: Remind tenants about rent due
**How**: Scheduler runs monthly, checks settings

### 5. Web Portal
**What**: Public shop listing and lead capture
**Why**: Allow tenants to browse and express interest
**How**: Custom web pages with no base template

### 6. Rent Receipt
**What**: Professional printable receipt
**Why**: Provide payment confirmation
**How**: Custom HTML print format

### 7. REST API
**What**: CRUD operations for Shop
**Why**: External system integration
**How**: Token-based authentication

### 8. Shops by Airport Report
**What**: Analytics on shop occupancy
**Why**: Track availability and revenue
**How**: SQL-based script report

---

## 🔧 Common Commands

### View Logs
```bash
bench --site localhost logs
```

### Clear Everything
```bash
bench --site localhost clear-cache
bench --site localhost clear-website-cache
bench build --apps airport
```

### Run Specific Scheduler
```bash
bench --site localhost execute airport.airport_shops.doctype.rent_contract.rent_contract.send_monthly_rent_reminders
```

### Import Fixtures Manually
```bash
bench --site localhost import-fixtures
```

### Check Background Jobs
```bash
bench --site localhost doctor
```

---

## 📖 Documentation Locations

- **Full Details**: `claude.md`
- **Summary**: `DAY_4_IMPLEMENTATION_SUMMARY.md`
- **API Docs**: `bruno_api_collection/README.md`
- **This Guide**: `QUICK_START.md`

---

## 🎯 Success Criteria

You'll know everything works when:

✅ Shop Types visible in system
✅ Gate number change updates tickets
✅ Web portal displays shop list
✅ Lead form submissions create records
✅ API requests return shop data
✅ Print format renders professionally
✅ Report shows occupancy stats

---

## 🆘 Quick Fixes

### Fixtures Not Loading?
```bash
bench --site localhost import-fixtures
```

### Web Portal 404?
```bash
bench --site localhost clear-website-cache
bench build --apps airport
```

### Background Job Not Running?
```bash
bench restart
```

### API Returns 401?
- Regenerate API keys
- Check format: `token key:secret`
- Verify credentials in header

---

## 💡 Pro Tips

1. **Testing Background Jobs**: Use a test flight with multiple tickets
2. **Web Portal**: Clear browser cache if CSS doesn't load
3. **API Testing**: Start with GET before POST
4. **Scheduler**: Won't run unless bench is started
5. **Print Format**: Test with actual Rent Payment data

---

## 🎓 What You Learned

- Background job patterns with `frappe.enqueue()`
- Scheduler configuration in hooks.py
- Fixtures for master data
- Client-side link filtering
- Web pages without base template
- Custom print formats
- REST API authentication
- Script report development

---

**Time to Complete**: ~5 minutes setup + ~10 minutes testing
**Difficulty**: Intermediate
**Framework**: Frappe v15

---

Ready? Start with Step 1! 🚀
