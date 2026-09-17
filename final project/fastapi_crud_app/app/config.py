"""Application configuration loaded from environment variables / .env file."""
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Immutable application settings."""

    app_name: str = os.getenv("APP_NAME", "Product Manager API")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    database_path: str = os.getenv("DATABASE_PATH", "products.db")


settings = Settings()
