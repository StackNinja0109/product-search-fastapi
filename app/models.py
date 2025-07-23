from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
  keyword: str

class ParserRequest(BaseModel):
  file_url: str
  formats: list[str]