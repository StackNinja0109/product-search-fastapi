import os
from typing import Dict, List
from amazon_paapi import AmazonApi as PAAPI
from fastapi import HTTPException, status

from app import AMAZON_PARTNER_TAG, AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_REGION

_products = {}

class AmazonAPI:
    def __init__(self):        
        self.api = PAAPI(
            AMAZON_ACCESS_KEY,
            AMAZON_SECRET_KEY,
            AMAZON_PARTNER_TAG,
            AMAZON_REGION
        )

    def search_products(self, jan_code: str) -> List[Dict]:
        if jan_code in _products:
            return _products[jan_code]
            
        try:
            response = self.api.search_items(keywords=jan_code, search_index='All')            
            products = []
            for item in response._items:
                product_details = {
                    'name': item._item_info._title._display_value,
                    'price': int(item._offers._listings[0]._price._amount) if item._offers and item._offers._listings else 0,
                    'image': item._images._primary._medium._url if item._images and item._images._primary else '',
                    'url': item.detail_page_url
                }
                products.append(product_details)
                
            products.sort(key=lambda x: x['price'])
            _products[jan_code] = products
            return products
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch data from Amazon API: {str(e)}"
            )

amazon_api = AmazonAPI()