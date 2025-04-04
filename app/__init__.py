import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN', '')

# YAHOO
YAHOO_CLIENT_ID = os.getenv('YAHOO_CLIENT_ID', '')
YAHOO_API_ENDPOINT = "https://shopping.yahooapis.jp/ShoppingWebService/V3"