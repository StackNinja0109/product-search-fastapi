import os
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.auth import authenticate_token
from app.models import SearchRequest
from app.handlers import handle_search

web_app = FastAPI(title="fastapi-skeleton", version="1.0.0", dependencies=[Depends(authenticate_token)])

origins = ["*"]
web_app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

@web_app.post("/v1/search")
async def search(request: SearchRequest):
  return await handle_search(request)

if __name__ == "__main__":
  is_reload = os.getenv("APP_ENV", "staging") == "staging"
  uvicorn.run("app.app:web_app", host="127.0.0.1", port=8000, reload=is_reload)