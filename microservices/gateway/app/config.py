from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    AUTH_URL: str = "http://auth_service:8000"
    EVENT_URL: str = "http://event_service:8000"
    SEAT_URL: str = "http://seat_service:8000"
    BOOKING_URL: str = "http://booking_service:8000"
    PAYMENT_URL: str = "http://payment_service:8000"

settings = Settings()