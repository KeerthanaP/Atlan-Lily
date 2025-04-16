# config/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file in the correct location
# For local development
local_env_path = os.path.join(os.path.dirname(__file__), ".env")
# For Docker environment
docker_env_path = "/app/config/.env"

# Try both paths
if os.path.exists(local_env_path):
    load_dotenv(local_env_path)
elif os.path.exists(docker_env_path):
    load_dotenv(docker_env_path)
else:
    print("Warning: .env file not found")

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SEARCH_ENGINE_URL = os.getenv("SEARCH_ENGINE_URL")
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    JWT_EXPIRATION_TIME = os.getenv("JWT_EXPIRATION_TIME", 3600)