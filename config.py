
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    rapidapi_proxy_secret: SecretStr = SecretStr("")
    rapidapi_allowed_subscriptions: str = "BASIC,PRO,ULTRA"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def rapidapi_allowed_plans(self) -> frozenset[str]:
        return frozenset(
            plan.strip().upper()
            for plan in self.rapidapi_allowed_subscriptions.split(",")
            if plan.strip()
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


# Convenience global variable — you can import `settings` directly
settings = get_settings()
