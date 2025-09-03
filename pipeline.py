from dotenv import load_dotenv
import os
import requests
import json

# Get Shopify domain and token from .env
load_dotenv()
DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN")
TOKEN = os.getenv("SHOPIFY_ADMIN_TOKEN")
if not DOMAIN or not TOKEN:
    raise RuntimeError("Missing SHOPIFY_STORE_DOMAIN or SHOPIFY_ADMIN_TOKEN")

headers = {"X-Shopify-Access-Token": TOKEN}
url = f"https://{DOMAIN}/admin/api/2025-07/orders.json"

response = requests.get(url, headers=headers, timeout=20)
print(response.status_code)
print(json.dumps(response.json(), indent=2))