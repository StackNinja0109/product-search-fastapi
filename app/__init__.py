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

# AMAZON
AMAZON_PARTNER_TAG = os.getenv('AMAZON_PARTNER_TAG', '')
AMAZON_ACCESS_KEY = os.getenv('AMAZON_ACCESS_KEY', '')
AMAZON_SECRET_KEY = os.getenv('AMAZON_SECRET_KEY', '')
AMAZON_REGION = os.getenv('AMAZON_REGION', '')

# LLAMA_PARSE & GEMINI
LLAMA_CLOUD_API_KEY = os.getenv('LLAMA_CLOUD_API_KEY', '')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_MODEL_NAME = os.getenv('GEMINI_MODEL_NAME', '')

if not YAHOO_CLIENT_ID:
  raise ValueError("YAHOO_CLIENT_ID environment variable is not set")

if not RAKUTEN_APP_ID:
  raise ValueError("RAKUTEN_APP_ID environment variable is not set")

if not all([AMAZON_PARTNER_TAG, AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY]):
  raise ValueError("Amazon API credentials not properly configured")

if not LLAMA_CLOUD_API_KEY:
  raise ValueError("LLAMA_CLOUD_API_KEY environment variable is not set")

if not all([GEMINI_API_KEY, GEMINI_MODEL_NAME]):
  raise ValueError("GEMINI_KEY environment variable is not set")