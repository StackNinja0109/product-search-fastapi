import os
from typing import Dict, List, Optional
import requests
from fastapi import HTTPException, status
from app import RAKUTEN_APP_ID, RAKUTEN_API_ENDPOINT

_products = {}

class RakutenAPI:
    def __init__(self):
        self.app_id = RAKUTEN_APP_ID
        self.endpoint = RAKUTEN_API_ENDPOINT

    def search_products(self, jan_code: str) -> List[Dict]:
        if jan_code in _products:
            return _products[jan_code]
        
        url = f"{self.endpoint}/IchibaItem/Search/20220601"

        params = {
            "applicationId": self.app_id,
            "keyword": jan_code,
            "format": "json"
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch data from Rakuten API"
            )
            
        data = response.json().get("Items")
        products = []
        for product in data:
            product_details = {
                'name': product.get('Item')['itemName'],
                'price': product.get('Item')['itemPrice'],
                'image': (product.get('Item').get('mediumImageUrls') or [{}])[0].get('imageUrl', ''),
                'url': product.get('Item')['itemUrl'],
            }
            products.append(product_details)

        products.sort(key=lambda x: x['price'])
        _products[jan_code] = products
        return products

rakuten_api = RakutenAPI()