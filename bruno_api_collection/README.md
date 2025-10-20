# Airport Management System - API Collection

This Bruno API collection contains example requests for interacting with the Airport Management System's REST API.

## Setup

### 1. Generate API Keys

1. Login to your Frappe site (http://localhost:8000)
2. Go to User menu → My Settings → API Access
3. Click "Generate Keys"
4. Copy the API Key and API Secret

### 2. Configure Environment

1. Open `environments/Local.bru`
2. Replace the placeholder values:
   ```
   api_key: your_actual_api_key
   api_secret: your_actual_api_secret
   ```

### 3. Import Collection to Bruno

1. Download and install Bruno from https://www.usebruno.com/
2. Open Bruno
3. Click "Open Collection"
4. Navigate to this folder (`bruno_api_collection`)
5. Select the collection

## Authentication

All API requests use Token-based authentication with the following header:

```
Authorization: token {api_key}:{api_secret}
```

Example:
```
Authorization: token abc123:xyz789
```

## Available Endpoints

### 1. GET All Shops
Retrieve all shops with all fields.

**Endpoint:** `GET /api/resource/Shop?fields=["*"]`

**Query Parameters:**
- `fields`: Array of field names (use `["*"]` for all fields)
- `filters`: JSON array of filters
- `limit_page_length`: Number of records per page
- `limit_start`: Offset for pagination

**Example:**
```bash
curl -X GET "http://localhost:8000/api/resource/Shop?fields=[\"*\"]" \
  -H "Authorization: token {api_key}:{api_secret}"
```

### 2. GET Shops (Filtered)
Retrieve shops with specific filters.

**Endpoint:** `GET /api/resource/Shop?filters=[["status","=","Available"]]`

**Filter Examples:**
- By status: `[["status","=","Available"]]`
- By airport: `[["airport","=","AIRPORT-001"]]`
- By area: `[["area",">",200]]`
- Multiple filters: `[["status","=","Available"],["area",">",200]]`

### 3. GET Shop by Name
Retrieve a specific shop by its document name.

**Endpoint:** `GET /api/resource/Shop/{shop_name}`

**Example:**
```bash
curl -X GET "http://localhost:8000/api/resource/Shop/SHOP-001" \
  -H "Authorization: token {api_key}:{api_secret}"
```

### 4. POST Create Shop
Create a new shop.

**Endpoint:** `POST /api/resource/Shop`

**Request Body:**
```json
{
  "shop_number": "S999",
  "shop_name": "Test Shop",
  "shop_type": "Normal",
  "status": "Available",
  "area": 300,
  "airport": "AIRPORT-001"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/resource/Shop" \
  -H "Authorization: token {api_key}:{api_secret}" \
  -H "Content-Type: application/json" \
  -d '{
    "shop_number": "S999",
    "shop_name": "Test Shop",
    "shop_type": "Normal",
    "status": "Available",
    "area": 300,
    "airport": "AIRPORT-001"
  }'
```

### 5. PUT Update Shop
Update an existing shop.

**Endpoint:** `PUT /api/resource/Shop/{shop_name}`

**Request Body (partial update):**
```json
{
  "status": "Occupied",
  "tenant": "TENANT-001"
}
```

### 6. DELETE Shop
Delete a shop.

**Endpoint:** `DELETE /api/resource/Shop/{shop_name}`

**Warning:** This action cannot be undone.

## Response Formats

### Success Response
```json
{
  "data": {
    "name": "SHOP-001",
    "shop_number": "S101",
    "status": "Available",
    // ... other fields
  }
}
```

### Error Response
```json
{
  "exception": "frappe.exceptions.ValidationError",
  "exc_type": "ValidationError",
  "_server_messages": "Error message here"
}
```

## Common HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Invalid or missing authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Testing the Collection

1. Ensure your Frappe site is running (`bench start`)
2. Configure your API keys in the environment file
3. Run requests in sequence:
   - First, get all shops to see existing data
   - Create a new shop with POST
   - Get the created shop by name
   - Update the shop with PUT
   - Delete the test shop with DELETE

## Additional Resources

- Frappe REST API Documentation: https://frappeframework.com/docs/user/en/api/rest
- Airport Management System Docs: See `/apps/airport/README.md`

## Support

For issues or questions:
- Check the Frappe Framework documentation
- Review the claude.md file in the app root for implementation details
- Contact the development team

## Notes

- All datetime values are in UTC format
- Currency values are in the default system currency (typically INR)
- Link fields require the document name (e.g., "AIRPORT-001"), not the display value
- Some fields are auto-generated and cannot be set during creation (e.g., `name`, `creation`, `modified`)
