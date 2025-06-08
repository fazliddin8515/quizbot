from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str = Field(default=..., alias="BOT_TOKEN")

    model_config = SettingsConfigDict(env_file=".env", populate_by_name=True)


settings = Settings()
