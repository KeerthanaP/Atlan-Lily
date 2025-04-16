from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.auth_service import AuthService
from datetime import timedelta
import os
from config.config import Config

router = APIRouter()

class TokenRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Initialize AuthService
auth_service = AuthService()

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(request: TokenRequest):
    """API to generate JWT token"""
    if request.username == "kprabhakaran" and request.password == "password":  # Mock validation
        access_token = auth_service.create_access_token(
            data={"sub": request.username}, 
            expires_delta=timedelta(minutes=30)  # Token expiry time
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
