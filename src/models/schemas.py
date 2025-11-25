"""
Módulo con los esquemas Pydantic para validación de requests y responses de la API.
Define los modelos de entrada y salida para los endpoints de FastAPI.
"""

from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class ChatRequest(BaseModel):
    """
    Modelo para recibir mensajes del usuario.
    """

    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Mensaje o pregunta del usuario",
        examples=["¿Cuál fue el resultado del último partido del Real Madrid?"],
    )
    session_id: Optional[str] = Field(
        default=None,
        description="ID de sesión para mantener contexto conversacional (opcional para MVP)",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "¿Cuáles son los partidos de hoy?",
                    "session_id": "user-123-session-456",
                }
            ]
        }
    }


class ChatResponse(BaseModel):
    """
    Modelo para respuestas del agente.
    """

    response: str = Field(..., description="Respuesta generada por el agente")
    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Nivel de confianza de la respuesta (0-1)",
    )
    sources: Optional[List[str]] = Field(
        default=None, description="Fuentes de información utilizadas"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Timestamp de la respuesta"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "response": "El Real Madrid ganó 3-1 contra el Barcelona.",
                    "confidence": 0.95,
                    "sources": ["API-Football", "ESPN"],
                    "timestamp": "2025-11-24T10:30:00",
                }
            ]
        }
    }


class MatchRecommendationRequest(BaseModel):
    """
    Modelo para solicitar recomendaciones sobre un partido específico.
    """

    home_team: str = Field(..., description="Equipo local", examples=["Real Madrid"])
    away_team: str = Field(..., description="Equipo visitante", examples=["Barcelona"])
    match_date: Optional[str] = Field(
        default=None, description="Fecha del partido (formato: YYYY-MM-DD)"
    )


class MatchRecommendationResponse(BaseModel):
    """
    Modelo para respuestas de recomendaciones de partidos.
    """

    recommendation: str = Field(
        ..., description="Recomendación del agente sobre el partido"
    )
    prediction: Optional[str] = Field(
        default=None, description="Predicción del resultado"
    )
    key_factors: Optional[List[str]] = Field(
        default=None, description="Factores clave considerados en la recomendación"
    )
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class HealthResponse(BaseModel):
    """
    Modelo para el endpoint de health check.
    """

    status: Literal["healthy", "unhealthy"] = Field(
        default="healthy", description="Estado de salud del servicio"
    )
    version: str = Field(default="1.0.0", description="Versión de la API")
    timestamp: datetime = Field(default_factory=datetime.now)
