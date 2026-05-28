from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    openai_api_key: str = "test-api-key"
    llm_base_url: str = "https://api.test.com/v1"
    model_name: str = "gpt-4o-mini"
    request_timeout: int = 30
    llm_temperature: float = 0.3
    cache_ttl: int = 300
    cache_maxsize: int = 100
    log_level: str = "INFO"

    model_config = {"env_file": ".env"}


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
