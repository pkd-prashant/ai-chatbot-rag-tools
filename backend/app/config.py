from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    groq_api_key: str
    alpha_vantage_api_key: str
    sqlite_path: str = "data/chatbot.db"
    embed_model: str = "nomic-embed-text"
    llm_model: str = "llama-3.1-8b-instant"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"
    )

settings = Settings()