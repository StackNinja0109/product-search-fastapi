from pydantic import BaseModel

class HelloRequest(BaseModel):
  content: str