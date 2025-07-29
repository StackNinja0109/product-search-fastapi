from fastapi import HTTPException, status
import asyncio

from app.models import SearchRequest, ParserRequest
from app.api.yahoo_api import yahoo_api
from app.api.rakuten_api import rakuten_api
from app.api.amazon_api import amazon_api

from llama_parse import LlamaParse
import google.generativeai as genai
from app import LLAMA_PARSE_API_KEY, GEMINI_API_KEY, GEMINI_MODEL_NAME

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
  file_name = request.file_url
  formats = request.formats

  genai.configure(api_key=GEMINI_API_KEY)
  model = genai.GenerativeModel(GEMINI_MODEL_NAME)

  parser = LlamaParse(
    api_key=LLAMA_PARSE_API_KEY,
    result_type="markdown",
#    premium_mode=True,
    use_vendor_multimodal_model=True,
    language="ja"
  )

  try:
    with open(file_name, "rb") as f:
      documents = parser.load_data(f, extra_info={"file_name": file_name})
      text = "".join([doc.text for doc in documents])

      prompt = (
        "あなたはPDFから表データを抽出するAIアシスタントです。\n"
        "以下の規則に従ってデータを抽出し、JSON配列形式で返してください：\n"
        "1. 表または罫線で区切られた部分のみを解析対象とします\n"
        "2. 各項目は1行として扱います\n"
        "3. 数量について：\n"
        "  - 単位（台、枚など）は除去し、数値のみを抽出\n"
        "  - 数量は正確性が最重要\n"
        "4. 複数品番の処理：\n"
        "  - 同一項目に複数品番がある場合、番号を付けて別行に分割\n"
        "  - 例：1①, 1②, 1③として出力\n"
        "5. 同等品の処理：\n"
        "  - \"同等\"という文字がある場合、同等品フラグを立てる\n"
        "6. 型番の処理：\n"
        "  - 英数字の組み合わせのみを抽出\n"
        "  - 日本語部分は品名に含める\n"
        "  - 同等品情報は除去\n"
        "7. 原本情報：\n"
        "  - 元の型番情報をそのまま保持する列を追加\n"
        "\n"
        "抽出する項目：\n"
        + "\n".join([f"- {item}" for item in formats]) +
        "\n\n"
        "以下の形式のJSONで回答してください：\n"
        "[\n"
        "  {\n"
        + ",\n".join([f'    "{item}": "値"' for item in formats]) +
        "\n  },\n"
        "  // 他のデータについても同様に\n"
        "]\n"
      )
      response = model.generate_content(prompt + text)
      
    return response.text
      
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Error parsing PDF: {str(e)}"
    )