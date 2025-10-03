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
    PDF内の「正式な注文表」に含まれるすべての行を**絶対に漏れなく抽出**してください。  

    【最重要ルール】  
    1. 出力は必ず有効なJSON配列のみとする。  
    2. JSON配列は必ず `[` で始まり `]` で終わり、その外側には一切文字を出さないこと。  
    3. JSON配列は1つだけ出力し、その中にすべての表データをまとめること。  
    4. JSON配列以外（文章・表記法・マークダウン・空行など）を含めないこと。  

    【抽出対象】  
    5. 「注文番号」「数量」「単価」「金額」が揃っている正式な注文表の行をすべて抽出する。  
    6. 注文表の途中で改行やセル結合があっても、必ず1行として結合して抽出する。  
    7. 表かどうか曖昧な場合でも、正式な注文表のパターンに合致する行はすべて抽出する。  
    8. 付属品・参考情報・明らかに注文表ではない行以外は除外しない。  

    【抽出ルール】  
    9. 各行を1つのオブジェクトとして抽出する。  
    10. 数量は単位（台・枚など）を除去して数値のみ抽出する。  
    11. 注文番号は英字・数字・-・/ の組み合わせとする。  
    12. 「同等」という文字が含まれる場合、"同等品可否": "同等品" を追加する。  
    13. 型番は英数字・-・/ のみを抽出し、日本語部分は品名に含める。  
    14. 文字列内の改行や空白はすべて結合して1行として扱う。  
    15. すべての正式な注文表の行を可能な限り抽出し、絶対に漏れがないようにする。  
    16. 抽出対象行は少しでも注文表の特徴があれば必ず含める。  

    【データ形式】  
    17. 数値（数量・単価・金額）は文字列として返す。必要に応じてカンマ区切りを使用できる。  
        - 例: 11100 → "11,100"、50 → "50"  

    【出力形式】  
    18. 出力は必ず以下の形式の JSON 配列とする：  
    [
        {{"\n{",\n".join([f'        "{item}": "値"' for item in formats])}\n    }},
        ...
    ]  

    【制約】  
    19. JSON配列以外を絶対に含めない。  
    20. JSON配列は必ず1つにまとめ、途中で分割したり複数個にしないこと。  
    21. すべての正式な注文表の行を漏れなく抽出すること。  
    22. 欠落や見逃しがないように、行が少しでも表の形式を満たす場合は必ず抽出する。  
  """

  try:
    start_time = time.time()
    result = await LlamaParse(
      parse_mode="parse_page_with_agent",
      model="openai-gpt-4-1-mini",
      high_res_ocr=True if target == "OCR" else False,
      adaptive_long_table=True,
      result_type="markdown",
      language="ja",
      user_prompt=prompt,
    ).aload_data(file_name)

    parsed_time = time.time()
    print(f"Parsed time: {parsed_time - start_time:.2f} seconds")

    processed_answers = []
    for doc in result:
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