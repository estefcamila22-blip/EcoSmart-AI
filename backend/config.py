import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "ESAI - EcoSmart AI"
    app_version: str = "0.1.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = environment == "development"
    api_prefix: str = "/api/v1"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/esai")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    mqtt_broker: str = os.getenv("MQTT_BROKER", "localhost")
    mqtt_port: int = int(os.getenv("MQTT_PORT", "1883"))
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = "gpt-4"
    whatsapp_api_url: str = os.getenv("WHATSAPP_API_URL", "https://graph.instagram.com/v18.0")
    whatsapp_phone_id: str = os.getenv("WHATSAPP_PHONE_ID", "")
    whatsapp_access_token: str = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
    polygon_rpc_url: str = os.getenv("POLYGON_RPC_URL", "https://polygon-rpc.com")
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    cors_origins: list = ["http://localhost:3000", "http://localhost:8080"]

settings = Settings()