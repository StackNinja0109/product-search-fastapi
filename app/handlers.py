from fastapi import HTTPException, status
import re

from app.models import SearchRequest
from app.api.yahoo_api import yahoo_api

async def handle_search_product(request: SearchRequest):
  keyword = request.keyword
  if not keyword:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Search keyword is required"
    )

  jan_code = yahoo_api.get_jan_code(keyword)
  products = yahoo_api.get_yahoo_product_details(jan_code)
  return products
  