import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN', '')

# YAHOO
YAHOO_CLIENT_ID = os.getenv('YAHOO_CLIENT_ID', '')
YAHOO_API_ENDPOINT = "https://shopping.yahooapis.jp/ShoppingWebService/V3"

# RAKUTEN
RAKUTEN_APP_ID = os.getenv('RAKUTEN_APP_ID', '')
RAKUTEN_API_ENDPOINT = "https://app.rakuten.co.jp/services/api"

if not YAHOO_CLIENT_ID:
  raise ValueError("YAHOO_CLIENT_ID environment variables is not set")

if not RAKUTEN_APP_ID:
  raise ValueError("RAKUTEN_APP_ID environment variables is not set")