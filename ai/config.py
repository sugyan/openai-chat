from pydantic import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    class Config:
        env_file = ".env"


settings = Settings()
