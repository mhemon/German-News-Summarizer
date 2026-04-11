from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_title: str = "German News Summarizer API"
    api_version: str = "0.1.0"
    debug: bool = True
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    app_url: str = "http://localhost:5173"

    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"

    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "openai/gpt-4o-mini"

    class Config:
        env_file = ".env"


settings = Settings()
