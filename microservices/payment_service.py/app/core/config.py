from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    BOOKING_URL: str = "http://127.0.0.1:8004"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

settings = Settings()