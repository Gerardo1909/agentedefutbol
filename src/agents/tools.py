"""
Herramientas (tools) para el agente de fútbol.
"""

from typing import Any, Optional, Dict

from langchain_core.tools import tool

from core.logging import agent_tools_logger
from services.football_info_service import (
    FootballInfoService,
    InvalidTeamError,
    InvalidLeagueError,
    MongoDBConnectionError,
    MongoDBQueryError,
)

_service = FootballInfoService()


@tool("get_upcoming_matches")
async def get_upcoming_matches(
    league: Optional[str] = None, team: Optional[str] = None, limit: int = 5
) -> Dict[str, Any]:
    """Obtiene próximos partidos de una liga O de un equipo.

    Args:
        league: Nombre de la liga (opcional). Ej: "Premier League", "La Liga", "Champions League"
        team: Nombre del equipo (opcional). Ej: "Manchester United", "Barcelona", "Real Madrid"
        limit: Número de partidos (por defecto 5, máximo 20)

    Importante: Debes proporcionar LEAGUE o TEAM, no ambos ni ninguno.
    """
    agent_tools_logger.info(
        f"Tool invocada: get_upcoming_matches - Liga: {league}, Equipo: {team}, Limit: {limit}"
    )

    # Validación de parámetros
    if not league and not team:
        agent_tools_logger.warning(
            "get_upcoming_matches: No se proporcionó league ni team"
        )
        return {
            "error": "Necesito saber de qué equipo o liga quieres ver los próximos partidos",
            "suggestion": "Por favor especifica un equipo o una liga",
        }

    if league and team:
        agent_tools_logger.warning(
            "get_upcoming_matches: Se proporcionaron ambos parámetros"
        )
        return {
            "error": "Solo puedo buscar por equipo O por liga, no ambos",
            "suggestion": "Especifica solo el equipo o solo la liga",
        }

    # Validar límite
    if limit < 1 or limit > 20:
        limit = min(max(limit, 1), 20)
        agent_tools_logger.info(f"Límite ajustado a: {limit}")

    try:
        # Buscar por equipo o por liga
        if team:
            result = await _service.get_team_upcoming_matches(team, limit)
        else:
            result = await _service.get_league_upcoming_matches(league, limit)

        agent_tools_logger.info(
            f"Tool completada: get_upcoming_matches - Resultados: {len(result)}"
        )

        if not result:
            return {
                "message": f"No encontré próximos partidos programados para {team or league}",
                "data": [],
            }

        return {"data": result}

    except InvalidTeamError as e:
        agent_tools_logger.warning(f"Equipo no válido: {team} - {str(e)}")
        return {
            "error": f"No encontré el equipo '{team}'",
            "suggestion": "Verifica que el nombre esté escrito correctamente",
        }

    except InvalidLeagueError as e:
        agent_tools_logger.warning(f"Liga no válida: {league} - {str(e)}")
        return {
            "error": f"No encontré la liga '{league}'",
            "suggestion": "Verifica que el nombre esté escrito correctamente",
        }

    except MongoDBConnectionError as e:
        agent_tools_logger.error(f"Error de conexión a MongoDB: {str(e)}")
        return {
            "error": "No puedo acceder a la base de datos en este momento",
            "suggestion": "Intenta nuevamente en unos momentos",
        }

    except MongoDBQueryError as e:
        agent_tools_logger.error(f"Error en consulta MongoDB: {str(e)}", exc_info=True)
        return {
            "error": "Hubo un problema al buscar los partidos",
            "suggestion": "Intenta reformular tu pregunta",
        }

    except Exception as e:
        agent_tools_logger.error(
            f"Error inesperado en get_upcoming_matches: {str(e)}", exc_info=True
        )
        return {
            "error": "Ocurrió un problema inesperado",
            "suggestion": "Por favor intenta de nuevo o contacta al administrador",
        }


@tool("get_match_results")
async def get_match_results(
    league: Optional[str] = None, team: Optional[str] = None, limit: int = 5
) -> Dict[str, Any]:
    """Obtiene resultados recientes de una liga O de un equipo.

    Args:
        league: Nombre de la liga (opcional). Ej: "Premier League", "La Liga"
        team: Nombre del equipo (opcional). Ej: "Manchester United", "Barcelona", "Real Madrid"
        limit: Número de resultados (por defecto 5, máximo 20)

    Importante: Debes proporcionar LEAGUE o TEAM, no ambos ni ninguno.
    """
    agent_tools_logger.info(
        f"Tool invocada: get_match_results - Liga: {league}, Equipo: {team}, Limit: {limit}"
    )

    # Validación de parámetros
    if not league and not team:
        agent_tools_logger.warning(
            "get_match_results: No se proporcionó league ni team"
        )
        return {
            "error": "Necesito saber de qué equipo o liga quieres ver los resultados",
            "suggestion": "Por favor especifica un equipo o una liga",
        }

    if league and team:
        agent_tools_logger.warning(
            "get_match_results: Se proporcionaron ambos parámetros"
        )
        return {
            "error": "Solo puedo buscar por equipo O por liga, no ambos",
            "suggestion": "Especifica solo el equipo o solo la liga",
        }

    # Validar límite
    if limit < 1 or limit > 20:
        limit = min(max(limit, 1), 20)
        agent_tools_logger.info(f"Límite ajustado a: {limit}")

    try:
        # Buscar por equipo o por liga
        if team:
            result = await _service.get_team_match_results(team, limit)
        else:
            result = await _service.get_league_match_results(league, limit)

        agent_tools_logger.info(
            f"Tool completada: get_match_results - Resultados: {len(result)}"
        )

        if not result:
            return {
                "message": f"No encontré resultados recientes para {team or league}",
                "data": [],
            }

        return {"data": result}

    except InvalidTeamError as e:
        agent_tools_logger.warning(f"Equipo no válido: {team} - {str(e)}")
        return {
            "error": f"No encontré el equipo '{team}'",
            "suggestion": "Verifica que el nombre esté escrito correctamente",
        }

    except InvalidLeagueError as e:
        agent_tools_logger.warning(f"Liga no válida: {league} - {str(e)}")
        return {
            "error": f"No encontré la liga '{league}'",
            "suggestion": "Verifica que el nombre esté escrito correctamente",
        }

    except MongoDBConnectionError as e:
        agent_tools_logger.error(f"Error de conexión a MongoDB: {str(e)}")
        return {
            "error": "No puedo acceder a la base de datos en este momento",
            "suggestion": "Intenta nuevamente en unos momentos",
        }

    except MongoDBQueryError as e:
        agent_tools_logger.error(f"Error en consulta MongoDB: {str(e)}", exc_info=True)
        return {
            "error": "Hubo un problema al buscar los resultados",
            "suggestion": "Intenta reformular tu pregunta",
        }

    except Exception as e:
        agent_tools_logger.error(
            f"Error inesperado en get_match_results: {str(e)}", exc_info=True
        )
        return {
            "error": "Ocurrió un problema inesperado",
            "suggestion": "Por favor intenta de nuevo o contacta al administrador",
        }


@tool("get_standings")
async def get_standings(league: str, season: Optional[str] = None) -> Dict[str, Any]:
    """Obtiene la tabla de posiciones de una liga.

    Args:
        league: Nombre de la liga (requerido). Ej: "Premier League", "La Liga"
        season: Temporada (opcional). Ej: "2025", "2024". Si no se especifica, usa la actual
    """
    agent_tools_logger.info(
        f"Tool invocada: get_standings - Liga: {league}, Temporada: {season}"
    )

    # Validación
    if not league:
        agent_tools_logger.warning("get_standings: No se proporcionó league")
        return {
            "error": "Necesito saber de qué liga quieres ver la tabla de posiciones",
            "suggestion": "Por favor especifica una liga",
        }

    try:
        result = await _service.get_standings(league, season)

        agent_tools_logger.info(
            f"Tool completada: get_standings - Posiciones: {len(result)}"
        )

        if not result:
            return {
                "message": f"No encontré la tabla de posiciones para {league}",
                "data": [],
            }

        return {"data": result}

    except InvalidLeagueError as e:
        agent_tools_logger.warning(f"Liga no válida: {league} - {str(e)}")
        return {
            "error": f"No encontré la liga '{league}'",
            "suggestion": "Verifica que el nombre esté escrito correctamente",
        }

    except MongoDBConnectionError as e:
        agent_tools_logger.error(f"Error de conexión a MongoDB: {str(e)}")
        return {
            "error": "No puedo acceder a la base de datos en este momento",
            "suggestion": "Intenta nuevamente en unos momentos",
        }

    except MongoDBQueryError as e:
        agent_tools_logger.error(f"Error en consulta MongoDB: {str(e)}", exc_info=True)
        return {
            "error": "Hubo un problema al buscar la tabla de posiciones",
            "suggestion": "Intenta reformular tu pregunta",
        }

    except Exception as e:
        agent_tools_logger.error(
            f"Error inesperado en get_standings: {str(e)}", exc_info=True
        )
        return {
            "error": "Ocurrió un problema inesperado",
            "suggestion": "Por favor intenta de nuevo o contacta al administrador",
        }


tools = [
    get_upcoming_matches,
    get_match_results,
    get_standings,
]
