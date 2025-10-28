from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
import stripe

class Settings(BaseSettings):
    stripe_secret_key: str
    stripe_publishable_key: str
    stripe_webhook_secret: str
    domain: str = "http://localhost:8000"  # Default for development

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

app = FastAPI()
stripe.api_key = settings.stripe_secret_key

@app.get("/")
def read_root():
    return {"message": "Stripe + FastAPI"}
