"""
Módulo con los endpoints de chat del agente de fútbol.
Define las rutas para interactuar con el chatbot mediante FastAPI.
"""

from typing import Optional
from fastapi import APIRouter, status, HTTPException, Depends
from core.logging import api_logger
from models.schemas import (
    ChatRequest,
    ChatResponse,
    MatchRecommendationRequest,
    MatchRecommendationResponse,
)
from agents.football_agent import FootballAgent

router = APIRouter(prefix="/api/v1/chat", tags=["Agente chat de fútbol."])


# TODO: Reemplazar con sistema de autenticación real (JWT, OAuth2, etc.)
async def get_current_user() -> Optional[str]:
    """
    Dependency para obtener el usuario actual.

    Returns:
        Nombre del usuario o None si no está autenticado
    """
    return "José"


def get_football_agent(
    user_name: Optional[str] = Depends(get_current_user),
) -> FootballAgent:
    """
    Factory para crear instancia del agente con contexto de usuario.

    Args:
        user_name: Nombre del usuario inyectado por dependency

    Returns:
        FootballAgent configurado para el usuario actual
    """
    api_logger.debug(f"Creando instancia de FootballAgent para usuario: {user_name}")
    return FootballAgent(user_name=user_name)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ChatResponse,
    summary="Endpoint para interactuar con el agente de fútbol",
    responses={
        200: {
            "description": "Respuesta exitosa del agente",
            "content": {
                "application/json": {
                    "example": {
                        "response": "El Bayern de Múnich es considerado uno de los mejores clubes de la historia. Ha ganado 6 Copas de Europa/Champions League y más de 30 títulos de Bundesliga, destacando por su dominio en Alemania y su éxito internacional.",
                        "confidence": 0.85,
                        "sources": ["Conocimiento del modelo"],
                        "used_tools": None,
                        "timestamp": "2025-11-25T16:30:00",
                    }
                }
            },
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error al procesar el mensaje: Connection timeout"
                    }
                }
            },
        },
    },
)
async def chat_endpoint(
    request: ChatRequest, agent: FootballAgent = Depends(get_football_agent)
):
    """
    Recibe un mensaje del usuario y devuelve una respuesta del agente.

    El agente puede responder preguntas sobre:
    - Resultados de partidos recientes
    - Próximos partidos y horarios
    - Estadísticas de equipos y jugadores
    - Noticias actuales del fútbol

    **Ejemplos de preguntas:**
    - "¿Cuál es el mejor equipo de la historia?"
    - "¿Quién es Lionel Messi?"
    - "Explícame la táctica 4-3-3"
    - "¿Qué equipos han ganado más Champions?"
    """
    api_logger.info(f"Request recibido en /chat - Session: {request.session_id}, Mensaje: {request.message[:100]}")
    try:
        response = await agent.process_message(
            message=request.message, session_id=request.session_id
        )
        api_logger.info(f"Respuesta generada exitosamente - Session: {request.session_id}, Tools usadas: {len(response.used_tools) if response.used_tools else 0}")
        return response

    except Exception as e:
        api_logger.error(f"Error en /chat endpoint - Session: {request.session_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el mensaje: {str(e)}",
        )


@router.post(
    "/recommend",
    status_code=status.HTTP_200_OK,
    response_model=MatchRecommendationResponse,
    summary="Obtener recomendación sobre un partido específico",
    responses={
        200: {
            "description": "Análisis exitoso del partido",
            "content": {
                "application/json": {
                    "example": {
                        "recommendation": "El Real Madrid llega con una racha de 5 victorias consecutivas, mientras que el Barcelona ha mostrado irregularidad con 2 derrotas en sus últimos 5 partidos. La ventaja de jugar en el Santiago Bernabéu es significativa para el Madrid.\n\nFactores clave:\n• Historial reciente favorable al Madrid (3 victorias en últimos 5 Clásicos)\n• Barcelona con lesiones en defensa\n• Momento anímico del Madrid superior\n\nPronóstico: Victoria ajustada del Real Madrid por 2-1, aprovechando su mejor momento y la ventaja de local.",
                        "prediction": "Análisis basado en conocimiento + herramientas",
                        "key_factors": [
                            "Forma reciente de los equipos",
                            "Historial de enfrentamientos",
                            "Ventaja de jugar en casa",
                        ],
                        "used_tools": ["get_team_stats", "get_upcoming_matches"],
                        "confidence": 0.85,
                    }
                }
            },
        },
        500: {
            "description": "Error al generar el análisis",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error al generar recomendación: Model unavailable"
                    }
                }
            },
        },
    },
)
async def match_recommendation_endpoint(
    request: MatchRecommendationRequest,
    agent: FootballAgent = Depends(get_football_agent),
):
    """
    Genera una recomendación y análisis detallado sobre un partido específico.

    El análisis incluye:
    - Forma reciente de ambos equipos
    - Historial de enfrentamientos directos
    - Ventaja del equipo local
    - Factores clave que pueden influir en el resultado
    - Predicción razonada del posible resultado

    **Ejemplo de uso:**
    ```json
    {
        "home_team": "Real Madrid",
        "away_team": "Barcelona",
        "match_date": "2025-12-01"
    }
    ```
    """
    api_logger.info(f"Request recibido en /recommend - Partido: {request.home_team} vs {request.away_team}, Fecha: {request.match_date}")
    try:
        response = await agent.analyze_match(
            home_team=request.home_team,
            away_team=request.away_team,
            match_date=request.match_date,
        )
        api_logger.info(f"Recomendacion generada exitosamente - Partido: {request.home_team} vs {request.away_team}, Tools usadas: {len(response.used_tools) if response.used_tools else 0}")
        return response

    except Exception as e:
        api_logger.error(f"Error en /recommend endpoint - Partido: {request.home_team} vs {request.away_team}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar recomendación: {str(e)}",
        )
