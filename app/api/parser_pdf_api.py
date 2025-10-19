from fastapi import HTTPException, status
from app.models import ParserRequest

import time
import json
from dotenv import load_dotenv

from llama_cloud_services import LlamaParse

load_dotenv()

async def parser_pdf_api(request: ParserRequest):
  start_time = time.time()

  parsing_files = request.urlLists
  formats = request.formats
  target = request.target
  parsing_numbers = request.numbers

  example_fields = ",\n".join([f'        "{item}": "〇〇〇"' for item in formats])
  prompt = f"""
  あなたはPDFから表データを抽出するAIアシスタントです。  
  PDF内の「正式な注文表」に含まれるすべての行を抽出してください。  
  【抽出対象】  
  1. 「注文番号」「数量」「単価」「金額」が揃っている正式な注文表の行をすべて抽出する。  
  2. 注文表の途中で改行やセル結合があっても、必ず1行として結合して抽出する。  
  3. 表かどうか曖昧な場合でも、正式な注文表のパターンに合致する行はすべて抽出する。  
  4. 付属品・参考情報・明らかに注文表ではない行以外は除外しない。  
  5. すべての正式な注文表の行を漏れなく抽出すること。  
  6. 欠落や見逃しがないように、行が少しでも表の形式を満たす場合は必ず抽出する。
  【抽出ルール】  
  1. 各行を1つのオブジェクトとして抽出する。  
  2. 数量は単位（台・枚など）を除去して数値のみ抽出する。  
  3. 注文番号は英字・数字・-・/ の組み合わせとする。  
  4. 「同等」という文字が含まれる場合、"同等品可否": "同等品" を追加する。  
  5. 型番は英数字・-・/ のみを抽出し、日本語部分は品名に含める。  
  6. すべての正式な注文表の行を可能な限り抽出し、絶対に漏れがないようにする。  
  7. 抽出対象行は少しでも注文表の特徴があれば必ず含める。  
  【データ形式】  
  1. 数値（数量・単価・金額）は文字列として返す。必要に応じてカンマ区切りを使用できる。  
      - 例: 11100 → "11,100"、50 → "50"  
  【出力形式】  
  1. 出力は必ず有効なJSON配列のみとする。  
  2. JSON配列は必ず `[` で始まり `]` で終わり、その外側には一切文字を出さないこと。  
  3. JSON配列は1つだけ出力し、その中にすべての表データをまとめること。  
  4. JSON配列以外（文章・表記法・マークダウン・空行など）を含めないこと。  
  5. JSON配列以外を絶対に含めない。  
  6. JSON配列は必ず1つにまとめ、途中で分割したり複数個にしないこと。  
  【出力例】  
  出力は必ず以下の形式の JSON 配列とする：
  ```
  [
    {{"\n{example_fields}\n    }},
    ...
  ]
  ```
  """

  try:
    start_time = time.time()
    results = await LlamaParse(
      parse_mode="parse_page_with_agent",
      target_pages=parsing_numbers if parsing_numbers != "" else None,
      model="openai-gpt-4-1-mini",
      high_res_ocr=True if target == "OCR" else False,
      adaptive_long_table=True,
      result_type="markdown",
      language="ja",
      user_prompt=prompt,
    ).aparse(parsing_files)

    documents = [res.get_markdown_documents(split_by_page=True) for res in results]
    processed_answers = []
    for document in documents:
      for doc in document:
        text = doc.text.strip()
        if text.startswith("[") and text.endswith("]"):
          try:
            processed_answers += json.loads(text)
          except Exception as e:
            print("JSON error:", e)
    
    parsed_time = time.time()
    print(f"Parsed time: {parsed_time - start_time:.2f} seconds")

    return processed_answers
      
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Error parsing PDF: {str(e)}"
    )