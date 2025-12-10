from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn, RedisDsn, Field


class Settings(BaseSettings):
    app_name: str = "AI Sales Automation"
    environment: str = Field("development", env="ENVIRONMENT")
    debug: bool = Field(True, env="DEBUG")

    database_url: PostgresDsn = Field(..., env="DATABASE_URL")
    redis_url: RedisDsn = Field(..., env="REDIS_URL")
    rabbitmq_url: str = Field(..., env="RABBITMQ_URL")

    openai_api_key: str = Field(..., env="OPENAI_API_KEY")

    odoo_api_url: str = Field(..., env="ODOO_API_URL")
    odoo_api_key: str = Field(..., env="ODOO_API_KEY")

    mcp_api_url: str = Field(..., env="MCP_API_URL")
    mcp_api_key: str = Field(..., env="MCP_API_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
