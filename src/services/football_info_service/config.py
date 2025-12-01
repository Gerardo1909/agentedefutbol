"""
Módulo que contiene la configuración del servicio de información de fútbol.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class FootballInfoServiceConfig(BaseSettings):
    """
    Configuración para el servicio de información de fútbol.
    Todas las variables deben estar definidas en el archivo .env
    """

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Configuración de MongoDB
    mongodb_uri: str
    mongodb_database: str
    mongodb_max_pool_size: int
    mongodb_min_pool_size: int
    mongodb_max_idle_time_ms: int
    mongodb_timeout_ms: int

    # Configuración de caché
    cache_ttl_upcoming_matches: int
    cache_ttl_past_matches: int
    cache_ttl_standings: int
