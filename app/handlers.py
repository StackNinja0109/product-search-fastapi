from fastapi import HTTPException, status
import re

from app.models import SearchRequest
from app.api.yahoo_api import yahoo_api
from app.api.rakuten_api import rakuten_api

async def handle_search_product(request: SearchRequest):
  keyword = request.keyword
  if not keyword:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Search keyword is required"
    )

  jan_code = yahoo_api.get_jan_code(keyword)
  yahoo_products = yahoo_api.search_products(jan_code)
  rakuten_products = rakuten_api.search_products(jan_code)

  print("jan_code: ", jan_code)
  
  return {
    "yahoo_products": yahoo_products,
    "rakuten_products": rakuten_products
  }
  