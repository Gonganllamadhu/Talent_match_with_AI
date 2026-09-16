import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

if ENV_FILE.exists():
    with open(ENV_FILE , "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                os.environ[key] = value


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "GenAI Resume Builder")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "genai_resume_builder_secret")
    MISTRAL_MODEL :str = os.getenv("MISTRAL_MODEL")
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SECRET_KEY = "HADUHAHsdhajdjaj38u3"
    
    # OpenAI & LLM Credentials

    CORS_ORIGINS: list = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:4200,http://127.0.0.1:4200,http://localhost:8000"
        ).split(",")
        if origin.strip()
    ]

settings = Settings()