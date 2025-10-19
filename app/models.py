from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
  keyword: str

class ParserRequest(BaseModel):
  urlLists: list[str]
  formats: list[str]
  target: str
  numbers: str