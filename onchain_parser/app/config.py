from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "dev"
    database_url: str
    bitcoin_rpc_url: str
    bitcoin_rpc_user: str
    bitcoin_rpc_password: str
    price_api_url: str = "https://api.coingecko.com/api/v3"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
