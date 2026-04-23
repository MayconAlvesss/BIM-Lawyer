import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Enterprise settings for BIM-Lawyer.
    Supports environment variable overrides.
    """
    PROJECT_NAME: str = "BIM-Lawyer"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"

    # Security
    API_KEY_NAME: str = "X-API-Key"
    API_KEY: str = "bim-lawyer-secure-key-2026"

    # Database / Vector
    CHROMA_DB_PATH: str = "database/chroma_sim"
    NORMS_DB_FILE: str = "database/norms_db.json"

    # LLM Settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
