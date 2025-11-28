"""
Herramientas (tools) para el agente de fútbol.

Este archivo define las herramientas que el agente podrá usar en futuras iteraciones.
Por ahora son stubs que retornan datos de ejemplo.
"""

from typing import Any, Dict, List

from langchain_core.tools import tool


@tool(
    "get_match_results",
    description="Obtiene los resultados recientes de un equipo de fútbol",
)
def get_match_results(team_name: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Obtiene los últimos resultados de un equipo.

    Args:
        team_name: Nombre del equipo
        limit: Número de resultados a obtener (por defecto 5)

    Returns:
        Lista de diccionarios con resultados de partidos
    """
    # TODO: Implementar integración con API-Football
    return [
        {
            "date": "2025-11-20",
            "opponent": "Equipo X",
            "score": "2-1",
            "result": "Victoria",
            "competition": "Liga",
        }
    ]


@tool("get_upcoming_matches", description="Obtiene los próximos partidos de un equipo")
def get_upcoming_matches(team_name: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Obtiene los próximos partidos programados para un equipo.

    Args:
        team_name: Nombre del equipo
        limit: Número de partidos a obtener (por defecto 5)

    Returns:
        Lista de diccionarios con próximos partidos
    """
    # TODO: Implementar integración con API-Football
    return [
        {
            "date": "2025-11-30",
            "opponent": "Equipo Y",
            "venue": "Casa",
            "competition": "Liga",
            "time": "20:00",
        }
    ]


@tool("get_team_stats", description="Obtiene estadísticas de un equipo de fútbol")
def get_team_stats(team_name: str, season: str = "2024-2025") -> Dict[str, Any]:
    """Obtiene estadísticas detalladas de un equipo.

    Args:
        team_name: Nombre del equipo
        season: Temporada (formato: YYYY-YYYY)

    Returns:
        Diccionario con estadísticas del equipo
    """
    # TODO: Implementar integración con API-Football
    return {
        "team": team_name,
        "season": season,
        "matches_played": 15,
        "wins": 10,
        "draws": 3,
        "losses": 2,
        "goals_for": 32,
        "goals_against": 15,
        "position": 3,
    }


@tool("get_player_stats", description="Obtiene estadísticas de un jugador de fútbol")
def get_player_stats(player_name: str, team_name: str = None) -> Dict[str, Any]:
    """Obtiene estadísticas detalladas de un jugador.

    Args:
        player_name: Nombre del jugador
        team_name: Nombre del equipo (opcional)

    Returns:
        Diccionario con estadísticas del jugador
    """
    # TODO: Implementar integración con API-Football
    return {
        "player": player_name,
        "team": team_name or "Equipo Ejemplo",
        "matches": 12,
        "goals": 8,
        "assists": 5,
        "yellow_cards": 2,
        "red_cards": 0,
    }


@tool("get_football_news", description="Obtiene noticias recientes sobre fútbol")
def get_football_news(query: str = "football", limit: int = 5) -> List[Dict[str, Any]]:
    """Obtiene noticias recientes relacionadas con el fútbol.

    Args:
        query: Término de búsqueda para las noticias
        limit: Número de noticias a obtener (por defecto 5)

    Returns:
        Lista de diccionarios con noticias
    """
    # TODO: Implementar integración con News API
    return [
        {
            "title": "Noticia de ejemplo sobre fútbol",
            "source": "Fuente Deportiva",
            "url": "https://example.com/noticia",
            "published_at": "2025-11-25T10:00:00Z",
            "description": "Esta es una noticia de ejemplo...",
        }
    ]


tools = [
    get_match_results,
    get_upcoming_matches,
    get_team_stats,
    get_player_stats,
    get_football_news,
]
