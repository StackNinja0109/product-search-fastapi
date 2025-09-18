from fastapi import HTTPException, status
from app.models import ParserRequest

import time
import json
from dotenv import load_dotenv

from llama_cloud_services import LlamaParse

load_dotenv()

async def parser_pdf_api(request: ParserRequest):
  start_time = time.time()

  file_name = request.file_url
  formats = request.formats
  target = request.target

  prompt = f"""
    あなたはPDFから表データを抽出するAIアシスタントです。  
		必ず以下のルールに従い、出力はテキストやマークダウン形式ではない有効なJSON配列のみを返してください。  

		【重要ルール】  
      1. 出力はテキストやマークダウン形式ではない有効なJSON 配列とする。  
      2. ```json やコメント、説明文は一切出力しないこと。  
      3. 英数字は半角で出力すること。  

		【解析対象】  
		  4. セルの境界線で区切られた表のみを対象とする。  

		【抽出ルール】  
      5. 各行を1項目として扱う。  
      6. 数量は単位（台・枚など）を除去し、数値のみを抽出する（数量の正確性を最優先）。  
      7. 注文番号は英字・数字・-・/ の組み合わせとする。  
      8. 「同等」という文字が含まれる場合、"同等品可否": "同等品" と設定する。  
      9. 型番は英数字・-・/ の組み合わせのみを抽出し、日本語部分は品名に含める。同等品に関する情報は除去する。  

		【データ形式】  
      10. 数値（数量・単価・金額）は文字列として返し、必要に応じてカンマ区切りを使用する。  
          - 例: 11100 → "11,100"、50 → "50"  

		【出力形式】  
		  11. 出力は必ず以下の形式の JSON 配列とする：  
          [
            {{
          {",\n".join([f'    "{item}": "値"' for item in formats])}
            }}
          ]

		【制約】  
      12. 出力には上記キーのみを含めること: {", ".join(formats)}  
      13. 表データ以外の内容は絶対に抽出しないこと。
    """

  try:
    start_time = time.time()
    result = await LlamaParse(
      parse_mode="parse_page_with_agent",
      model="openai-gpt-4-1-mini",
      high_res_ocr=True if target == "画像分析" else False,
      adaptive_long_table=True,
      result_type="markdown",
      language="ja",
      user_prompt=prompt,
    ).aparse(file_name)

    documents = result.get_markdown_documents(split_by_page=True)

    parsed_time = time.time()
    print(f"Parsed time: {parsed_time - start_time:.2f} seconds")

    processed_answers = []
    for i, doc in enumerate(documents):
      text = doc.text.strip()
      if text.startswith("[") and text.endswith("]"):
        answer = json.loads(text)
        if len(answer) > 0:
          processed_answers.extend(answer)

    return processed_answers
      
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Error parsing PDF: {str(e)}"
    )