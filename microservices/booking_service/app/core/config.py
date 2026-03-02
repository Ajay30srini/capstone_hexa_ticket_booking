from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    EVENT_URL: str = "http://127.0.0.1:8002"
    SEAT_URL: str = "http://127.0.0.1:8003"

settings = Settings()