from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from config.config import Config
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
# OAuth2 scheme used to extract the token from headers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthService:
    def __init__(self):
        """
        Initialize the AuthService with JWT secret, algorithm, and expiration time.
        """
        self.secret_key = Config.JWT_SECRET
        self.algorithm = Config.JWT_ALGORITHM
        self.expiration_time = int(Config.JWT_EXPIRATION_TIME)  # Default to 1 hour if not set

        # Ensure that critical environment variables are set
        if not self.secret_key or not self.algorithm:
            raise ValueError("Missing JWT_SECRET or JWT_ALGORITHM in environment variables.")

    def create_access_token(self, data: dict, expires_delta: timedelta):
        """
        Create a new access token.
        :param data: The data to encode in the JWT token.
        :param expiry_time: timedelta for token expiration
        :return: The encoded JWT token.
        """
        to_encode = data.copy()
        expiration = datetime.utcnow() + timedelta(seconds=self.expiration_time)
        to_encode.update({"exp": expiration})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str):
        """
        Verify the JWT token and return the payload.
        :param token: The JWT token to verify.
        :return: The decoded payload if the token is valid.
        :raises HTTPException: If the token is invalid or expired.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

    def get_current_user(self, request: Request):
        """
        Get the current user from the request.
        :param request: The HTTP request object.
        :return: The user information if the token is valid.
        :raises HTTPException: If the token is invalid or expired.
        """
        token = request.headers.get("Authorization")
        if token:
            token = token.split(" ")[1]
        else:
            raise HTTPException(status_code=403, detail="Not authenticated")
        
        return
