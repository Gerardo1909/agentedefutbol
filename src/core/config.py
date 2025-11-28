"""
Configuración centralizada del proyecto.
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configuración de la aplicación."""

    # LLM Configuration
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", ""))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", ""))

    # API Configuration
    API_TITLE: str = "Agente de Fútbol"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API para interactuar con un agente de fútbol basado en IA"

    # External APIs (para futuras implementaciones)
    FOOTBALL_API_KEY: Optional[str] = os.getenv("FOOTBALL_API_KEY")


settings = Settings()
