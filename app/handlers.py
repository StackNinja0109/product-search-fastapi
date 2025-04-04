from fastapi import HTTPException, status
from app.models import SearchRequest

async def handle_search(request: SearchRequest):
  if not request.keyword:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Search keyword is required"
    )