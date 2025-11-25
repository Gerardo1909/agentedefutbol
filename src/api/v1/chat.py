"""
Módulo con los endpoints de chat del agente de fútbol.
Define las rutas para interactuar con el chatbot mediante FastAPI.
"""

from fastapi import APIRouter, status, HTTPException
from models.schemas import (
    ChatRequest,
    ChatResponse,
    MatchRecommendationRequest,
    MatchRecommendationResponse,
)

router = APIRouter(prefix="/api/v1/chat", tags=["Agente chat de fútbol."])


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ChatResponse,
    summary="Endpoint para interactuar con el agente de fútbol",
)
async def chat_endpoint(request: ChatRequest):
    """
    Recibe un mensaje del usuario y devuelve una respuesta del agente.

    El agente puede responder preguntas sobre:
    - Resultados de partidos recientes
    - Próximos partidos y horarios
    - Estadísticas de equipos y jugadores
    - Noticias actuales del fútbol
    """
    # TODO: Implementar la integración con el agente de fútbol 
    response_text = "Hola, soy tu agente de fútbol. ¿En qué puedo ayudarte?"
    return ChatResponse(response=response_text, confidence=0.8, sources=["Sistema"])


@router.post(
    "/recommend",
    status_code=status.HTTP_200_OK,
    response_model=MatchRecommendationResponse,
    summary="Obtener recomendación sobre un partido específico",
)
async def match_recommendation_endpoint(request: MatchRecommendationRequest):
    """
    Genera una recomendación basada en estadísticas y datos del partido.
    """
    # TODO: Implementar lógica de recomendación con el agente
    recommendation_text = (
        f"Análisis del partido {request.home_team} vs {request.away_team}: "
        "Basado en las estadísticas recientes..."
    )
    return MatchRecommendationResponse(
        recommendation=recommendation_text,
        prediction="Pendiente de implementación",
        key_factors=["Forma reciente", "Historial de enfrentamientos"],
        confidence=0.7,
    )
