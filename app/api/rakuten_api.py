import os
from typing import Dict, List, Optional
import requests
import aiohttp
from fastapi import HTTPException, status
from app import RAKUTEN_APP_ID, RAKUTEN_API_ENDPOINT

_products = {}

class RakutenAPI:
    def __init__(self):
        self.app_id = RAKUTEN_APP_ID
        self.endpoint = RAKUTEN_API_ENDPOINT

    async def search_products(self, jan_code: str) -> List[Dict]:
        if jan_code in _products:
            return _products[jan_code]
        
        url = f"{self.endpoint}/IchibaItem/Search/20220601"

        params = {
            "applicationId": self.app_id,
            "keyword": jan_code,
            "format": "json"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                       print("Failed to fetch data from Rakuten API")
                       _products[jan_code] = []
                       return []
                       
                    data = await response.json()
                    items = data.get("Items", [])
                    products = []
                   
                    for product in items:
                        item = product.get('Item', {})
                        product_details = {
                           'name': item.get('itemName'),
                           'price': item.get('itemPrice'),
                           'image': (item.get('mediumImageUrls') or [{}])[0].get('imageUrl', ''),
                           'url': item.get('itemUrl'),
                           'platform': '楽天市場',
                        }
                        products.append(product_details)
                    products.sort(key=lambda x: x['price'])
                    _products[jan_code] = products
                    return products
                   
        except Exception as e:
            print(f"An error occurred: {e}")
            _products[jan_code] = []
            return []

rakuten_api = RakutenAPI()