from fastapi import HTTPException, status
import asyncio

from app.models import SearchRequest, ParserRequest
from app.api.yahoo_api import yahoo_api
from app.api.rakuten_api import rakuten_api
from app.api.amazon_api import amazon_api

from app.api.parser_pdf_api import parser_pdf_api

async def handle_search_product(request: SearchRequest):
  keyword = request.keyword
  if not keyword:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Search keyword is required"
    )

  yahoo_products = []
  rakuten_products = []
  amazon_products = []

  jan_code = yahoo_api.get_jan_code(keyword)
  if jan_code:
    tasks = [
        yahoo_api.search_products(jan_code),
        rakuten_api.search_products(jan_code),
        amazon_api.search_products(jan_code)
    ]

    yahoo_products, rakuten_products, amazon_products = await asyncio.gather(*tasks)
  
  return {
    "jan_code": jan_code,
    "yahoo_products": yahoo_products,
    "rakuten_products": rakuten_products,
    "amazon_products": amazon_products
  }
  


async def handle_parser_pdf(request: ParserRequest):
  result = await parser_pdf_api(request=request)
  return result
  


  