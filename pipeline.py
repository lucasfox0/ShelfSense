from dotenv import load_dotenv
from google.cloud import bigquery   
import os
import requests
import json

# Load shopify credentials from .env
load_dotenv()
DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN")
TOKEN = os.getenv("SHOPIFY_ADMIN_TOKEN")
if not DOMAIN or not TOKEN:
    raise RuntimeError("Missing SHOPIFY_STORE_DOMAIN or SHOPIFY_ADMIN_TOKEN")

# Make a GET request to the Shopify Admin REST API to fetch order data
headers = {"X-Shopify-Access-Token": TOKEN}
url = f"https://{DOMAIN}/admin/api/2025-07/orders.json"
response = requests.get(url, headers=headers, timeout=20)
data = response.json()
print(response.status_code)
# print(json.dumps(data, indent=2))

# Initalize directories:
#   - sales_totals: total units sold per variant
#   - product_info: product metadata (name, sku) keyed by variant_id
#   - daily_sales: total units sold per day (YY-MM-DD)
sales_totals = {}
product_info = {}
daily_sales = {}

# Iterate over all orders and their line items
for order in data.get("orders", []):
    for item in order.get("line_items", []):
        var_id = item.get("variant_id")
        if var_id is None: # Skip if theres no variant_id 
            continue

        qty = item.get("quantity", 0)
        name = item.get("name", "NA")
        sku = item.get("sku", "NA")
        date = order.get("created_at", "NA")[:10] # Extract order date (YY-MM-DD)

        # Accumulate total units per variant
        sales_totals[var_id] = sales_totals.get(var_id, 0) + qty

        # Store product metadata which will be nice for displaying
        # Want to fix this eventually so it isn't constantly overwriting, safe for now though.
        product_info[var_id] = {"name": name, "sku": sku}

        # Accumulate total units sold per day
        daily_sales[date] = daily_sales.get(date, 0) + qty

# Print summary table of top-selling variants (sorted by units sold, descending)
sorted_var_ids = sorted(sales_totals, key=sales_totals.get, reverse=True)
print("| UNITS |     NAME                                          |   SKU   |   VARIANT_ID   |")
for var in sorted_var_ids:
    print(f" {sales_totals[var]}   {product_info[var].get("name")}   {product_info[var].get("sku")}   {var}")

# Print summary table of daily sales (sorted by most recent date first)
print("\n|  DATE  |  UNITS SOLD  |")
for date in sorted(daily_sales, reverse=True):
    print(f"{date}   {daily_sales[date]}")