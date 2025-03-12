from pydantic import BaseModel
from functools import lru_cache
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'postgresql://postgres:admin@localhost:5432/multitenancy')
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-super-secret-key-here')
    ALGORITHM: str = os.getenv('ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 