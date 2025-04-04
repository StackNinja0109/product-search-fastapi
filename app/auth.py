import os
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from app import API_TOKEN

bearer_scheme = HTTPBearer(auto_error=False)

async def authenticate_token(token: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)):
  if not token or token.credentials != API_TOKEN:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
    )