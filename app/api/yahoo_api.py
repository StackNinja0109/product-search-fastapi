import requests
from collections import Counter
from app import YAHOO_CLIENT_ID, YAHOO_API_ENDPOINT

_janCodes = {}
_products = {}

class YahooAPI:
    def __init__(self):
        self.client_id = YAHOO_CLIENT_ID
        self.endpoint = YAHOO_API_ENDPOINT

    def get_jan_code(self, keyword):
        """ Get Jan Code using Yahoo Shopping API V3 """
        
        if keyword in _janCodes:
            return _janCodes[keyword]

        url = f"{self.endpoint}/itemSearch"
        
        headers = {
            'Authorization': f'Bearer {self.client_id}',
            'Content-Type': 'application/json'
        }
        
        params = {
            'query': keyword,
            'appid': self.client_id,
            'sort': '+price'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()            
            data = response.json()
            janCodes = []
            
            if 'hits' in data and data['hits']:
                for product in data['hits']:
                    janCode = product.get('janCode')
                    if janCode:
                        janCodes.append(janCode)
                        
            most_janCode = Counter(janCodes).most_common(1)[0][0] if len(janCodes) else None
            _janCodes[keyword] = most_janCode
            
            return most_janCode
            
        except requests.RequestException as e:
            print(f"API request error: {e}")
            return None
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def get_yahoo_product_details(self, jan_code, max_results=20):
        """
        Get detailed product information using Yahoo Shopping API V3
        """
        if jan_code in _products:
            return _products[jan_code]

        url = f"{self.endpoint}/itemSearch"
        
        headers = {
            'Authorization': f'Bearer {self.client_id}',
            'Content-Type': 'application/json'
        }
        
        params = {
            'query': jan_code,
            'appid': self.client_id,
            'results': max_results,
            'sort': '+price'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            products = []
            
            if 'hits' in data and data['hits']:
                for product in data['hits']:
                    product_details = {
                        'name': product.get('name'),
                        'description': product.get('description'),
                        'url': product.get('url'),
                        'image': product.get('image', []),
                        'price': product.get('price'),
                        'title': product.get('name'),
                    }
                    products.append(product_details)

            _products[jan_code] = products
            return products
            
        except requests.RequestException as e:
            print(f"API request error: {e}")
            return None
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

yahoo_api = YahooAPI()