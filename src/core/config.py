from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    DEBUG: bool = False

    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "mydb"

    model_config = {
        "env_file": ".env"
    }

settings = Settings()