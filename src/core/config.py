"""
Configuración centralizada del proyecto.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Configuración de la aplicación."""

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Configuración del agente groq
    groq_api_key: str
    groq_model: str
    temperature: float
    max_retries: int

    # Detalles de la API
    api_title: str = "Agente de Fútbol"
    api_version: str = "1.0.0"
    api_description: str = "API para interactuar con un agente de fútbol basado en IA"
