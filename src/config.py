from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")

    name: str = "urlshortener"
    debug_level: str = "INFO"


class MySQLSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="MYSQL_")

    host: str = "127.0.0.1"
    port: int = 3306
    user: str = "root"
    password: str = ""
    database: str = "url_shortener"
    pool_min: int = 1
    pool_max: int = 10
