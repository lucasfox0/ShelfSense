from dotenv import load_dotenv
import os

# Get Shopify domain and token from .env
load_dotenv()
DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN")
TOKEN = os.getenv("SHOPIFY_ADMIN_TOKEN")

if not DOMAIN or not TOKEN:
    raise RuntimeError("Missing SHOPIFY_STORE_DOMAIN or SHOPIFY_ADMIN_TOKEN")

print("Env loaded ", DOMAIN)