# services/auth_service.py
from fastapi import HTTPException, status
import jwt
from config.constants import JWT_SECRET, JWT_ALGORITHM

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
