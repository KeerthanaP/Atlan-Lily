# services/auth_service.py
from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from config.config import Config
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# This service handles authentication and JWT token management.
class AuthService:
    def __init__(self):
        """
        @summary: Initialize the AuthService with JWT secret and algorithm.
        """
        self.secret_key = os.getenv("JWT_SECRET")
        self.algorithm = os.getenv("JWT_ALGORITHM")
        self.expiration_time = 3600  # 1 hour
    
    def create_access_token(self, data: dict):
        """
        @summary: Create a new access token.
        @param data: The data to encode in the JWT token.   
        @return: The encoded JWT token.
        """
        to_encode = data.copy()
        expiration = datetime.utcnow() + timedelta(seconds=self.expiration_time)
        to_encode.update({"exp": expiration})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str):
        """
        @summary: Verify the JWT token and return the payload.  
        @param token: The JWT token to verify.
        @return: The decoded payload if the token is valid.
        @raises HTTPException: If the token is invalid or expired.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

    def get_current_user(self, request: Request):
        """
        @summary: Get the current user from the request.    
        @param request: The HTTP request object.
        @return: The user information if the token is valid.
        @raises HTTPException: If the token is invalid or expired.
        """
        token = request.headers.get("Authorization")
        if token:
            token = token.split(" ")[1]
        else:
            raise HTTPException(status_code=403, detail="Not authenticated")
        
        return self.verify_token(token)
