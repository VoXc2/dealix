from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Dealix API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql://dealix:DealixDbPass2026@db:5432/dealix"
    REDIS_URL: str = "redis://redis:6379/0"
    JWT_SECRET: str = "dealix-super-secret-2026"
    JWT_ALGORITHM: str = "HS256"
    CORS_ORIGINS: list = ["http://localhost:9001"]
    ADMIN_EMAIL: str = "admin@dealix.sa"
    ADMIN_PASSWORD: str = "Admin123456"
    class Config:
        env_file = ".env"

settings = Settings()
