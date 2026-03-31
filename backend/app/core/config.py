"""Dealix - Application Settings"""
from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Dealix"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-change-in-production-9f8e7d6c5b4a"
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    DATABASE_URL: str = "postgresql+asyncpg://dealix:dealix123@localhost:5432/dealix"
    DATABASE_URL_SYNC: str = "postgresql://dealix:dealix123@localhost:5432/dealix"
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    JWT_SECRET_KEY: str = "jwt-dev-secret-change-me-a1b2c3d4"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_NAME: str = "Dealix"
    SMTP_FROM_EMAIL: str = "noreply@dealix.sa"
    SMTP_USE_TLS: bool = True

    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None

    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_PUBLIC_KEY: Optional[str] = None

    DEFAULT_CURRENCY: str = "SAR"
    DEFAULT_LOCALE: str = "ar_SA"
    DEFAULT_TIMEZONE: str = "Asia/Riyadh"

    DEAL_STAGES: List[str] = [
        "new", "contacted", "qualified", "proposal",
        "negotiation", "closed_won", "closed_lost"
    ]
    LEAD_SOURCES: List[str] = [
        "website", "referral", "social_media", "google_ads",
        "cold_call", "email_campaign", "affiliate", "event", "other"
    ]
    COMMISSION_TYPES: List[str] = ["percentage", "fixed", "tiered"]

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
