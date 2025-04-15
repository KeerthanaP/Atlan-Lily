# config/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SEARCH_ENGINE_URL = os.getenv("SEARCH_ENGINE_URL")
