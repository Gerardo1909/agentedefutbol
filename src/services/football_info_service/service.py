"""
Módulo del servicio de información de fútbol.
Proporciona funcionalidades para obtener partidos próximos, resultados y clasificaciones.
"""

from datetime import datetime
from typing import Any, Optional, List, Dict

from core.logging import football_service_logger
from services.football_info_service.config import FootballInfoServiceConfig
from services.football_info_service.cache.memory_cache import MemoryCache
from services.football_info_service.resolvers import LeagueResolver, TeamResolver
from services.football_info_service.source_client.mongodb_client import MongoDBClient
from services.football_info_service.models import MongoDBConfig
from services.football_info_service.exceptions import (
    InvalidTeamError,
    InvalidLeagueError,
)


class FootballInfoService:
    """
    Servicio para la obtención de información de fútbol.
    """

    def __init__(self):
        self.config = FootballInfoServiceConfig()
        self.memory_cache = MemoryCache()
        self.league_resolver = LeagueResolver()
        self.team_resolver = TeamResolver()

        # Configurar cliente MongoDB
        mongo_config = MongoDBConfig(
            uri=self.config.mongodb_uri,
            database_name=self.config.mongodb_database,
            max_pool_size=self.config.mongodb_max_pool_size,
            min_pool_size=self.config.mongodb_min_pool_size,
            max_idle_time_ms=self.config.mongodb_max_idle_time_ms,
            timeout_ms=self.config.mongodb_timeout_ms,
        )
        self.mongodb_client = MongoDBClient(mongo_config)

    async def get_team_upcoming_matches(
        self, team_name: Optional[str] = None, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Obtiene los próximos partidos de un equipo.

        Raises:
            InvalidTeamError: Si el equipo no se puede resolver
            MongoDBConnectionError: Si hay problemas de conexión
            MongoDBQueryError: Si falla la consulta a MongoDB
        """
        football_service_logger.info(
            f"Obteniendo proximos partidos para equipo: {team_name}, Limit: {limit}"
        )

        if not team_name:
            football_service_logger.warning("No se proporcionó nombre de equipo")
            return []

        # Resolver ID del equipo
        team_id = self.team_resolver.resolve(team_name)
        if team_id is None:
            football_service_logger.warning(f"Equipo no encontrado: {team_name}")
            raise InvalidTeamError(f"No se pudo resolver el equipo: {team_name}")

        # Intentar obtener desde caché
        cache_key = f"upcoming:team:{team_id}:{limit}"
        cached_data = await self.memory_cache.get(cache_key)
        if cached_data is not None:
            football_service_logger.info(f"Datos obtenidos desde caché: {cache_key}")
            return cached_data

        # Consultar MongoDB
        matches = await self.mongodb_client.get_upcoming_fixtures(
            team_id=team_id, limit=limit
        )

        # Convertir a diccionarios
        result = [match.model_dump(by_alias=False) for match in matches]

        # Guardar en caché
        await self.memory_cache.set(
            cache_key, result, ttl=self.config.cache_ttl_upcoming_matches
        )

        return result

    async def get_league_upcoming_matches(
        self, league_name: Optional[str] = None, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Obtiene los próximos partidos de una liga.

        Raises:
            InvalidLeagueError: Si la liga no se puede resolver
            MongoDBConnectionError: Si hay problemas de conexión
            MongoDBQueryError: Si falla la consulta a MongoDB
        """
        football_service_logger.info(
            f"Obteniendo proximos partidos para liga: {league_name}, Limit: {limit}"
        )

        if not league_name:
            football_service_logger.warning("No se proporcionó nombre de liga")
            return []

        # Resolver ID de la liga
        league_id = self.league_resolver.resolve(league_name)
        if league_id is None:
            football_service_logger.warning(f"Liga no encontrada: {league_name}")
            raise InvalidLeagueError(f"No se pudo resolver la liga: {league_name}")

        # Intentar obtener desde caché
        cache_key = f"upcoming:league:{league_id}:{limit}"
        cached_data = await self.memory_cache.get(cache_key)
        if cached_data is not None:
            football_service_logger.info(f"Datos obtenidos desde caché: {cache_key}")
            return cached_data

        # Consultar MongoDB
        matches = await self.mongodb_client.get_upcoming_fixtures(
            league_id=league_id, limit=limit
        )

        # Convertir a diccionarios
        result = [match.model_dump(by_alias=False) for match in matches]

        # Guardar en caché
        await self.memory_cache.set(
            cache_key, result, ttl=self.config.cache_ttl_upcoming_matches
        )

        return result

    async def get_team_match_results(
        self, team_name: Optional[str] = None, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Obtiene los resultados de los últimos partidos de un equipo.

        Raises:
            InvalidTeamError: Si el equipo no se puede resolver
            MongoDBConnectionError: Si hay problemas de conexión
            MongoDBQueryError: Si falla la consulta a MongoDB
        """
        football_service_logger.info(
            f"Obteniendo resultados de últimos partidos para equipo: {team_name}, Limit: {limit}"
        )

        if not team_name:
            football_service_logger.warning("No se proporcionó nombre de equipo")
            return []

        # Resolver ID del equipo
        team_id = self.team_resolver.resolve(team_name)
        if team_id is None:
            football_service_logger.warning(f"Equipo no encontrado: {team_name}")
            raise InvalidTeamError(f"No se pudo resolver el equipo: {team_name}")

        # Intentar obtener desde caché
        cache_key = f"past:team:{team_id}:{limit}"
        cached_data = await self.memory_cache.get(cache_key)
        if cached_data is not None:
            football_service_logger.info(f"Datos obtenidos desde caché: {cache_key}")
            return cached_data

        # Consultar MongoDB
        matches = await self.mongodb_client.get_past_fixtures(
            team_id=team_id, limit=limit
        )

        # Convertir a diccionarios
        result = [match.model_dump(by_alias=False) for match in matches]

        # Guardar en caché
        await self.memory_cache.set(
            cache_key, result, ttl=self.config.cache_ttl_past_matches
        )

        return result

    async def get_league_match_results(
        self, league_name: Optional[str] = None, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Obtiene los resultados de los últimos partidos de una liga.

        Raises:
            InvalidLeagueError: Si la liga no se puede resolver
            MongoDBConnectionError: Si hay problemas de conexión
            MongoDBQueryError: Si falla la consulta a MongoDB
        """
        football_service_logger.info(
            f"Obteniendo resultados de últimos partidos para liga: {league_name}, Limit: {limit}"
        )

        if not league_name:
            football_service_logger.warning("No se proporcionó nombre de liga")
            return []

        # Resolver ID de la liga
        league_id = self.league_resolver.resolve(league_name)
        if league_id is None:
            football_service_logger.warning(f"Liga no encontrada: {league_name}")
            raise InvalidLeagueError(f"No se pudo resolver la liga: {league_name}")

        # Intentar obtener desde caché
        cache_key = f"past:league:{league_id}:{limit}"
        cached_data = await self.memory_cache.get(cache_key)
        if cached_data is not None:
            football_service_logger.info(f"Datos obtenidos desde caché: {cache_key}")
            return cached_data

        # Consultar MongoDB
        matches = await self.mongodb_client.get_past_fixtures(
            league_id=league_id, limit=limit
        )

        # Convertir a diccionarios
        result = [match.model_dump(by_alias=False) for match in matches]

        # Guardar en caché
        await self.memory_cache.set(
            cache_key, result, ttl=self.config.cache_ttl_past_matches
        )

        return result

    async def get_standings(
        self, league_name: str, season: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene la clasificación de una liga en una temporada específica.

        Raises:
            InvalidLeagueError: Si la liga no se puede resolver
            MongoDBConnectionError: Si hay problemas de conexión
            MongoDBQueryError: Si falla la consulta a MongoDB
        """
        football_service_logger.info(
            f"Obteniendo clasificacion - Liga: {league_name}, Temporada: {season}"
        )

        if not league_name:
            football_service_logger.warning("No se proporcionó nombre de liga")
            return []

        # Resolver ID de la liga
        league_id = self.league_resolver.resolve(league_name)
        if league_id is None:
            football_service_logger.warning(f"Liga no encontrada: {league_name}")
            raise InvalidLeagueError(f"No se pudo resolver la liga: {league_name}")

        # Usar temporada actual si no se proporciona
        if season is None:
            season = self._current_season()

        # Intentar obtener desde caché
        cache_key = f"standings:league:{league_id}:{season}"
        cached_data = await self.memory_cache.get(cache_key)
        if cached_data is not None:
            football_service_logger.info(f"Datos obtenidos desde caché: {cache_key}")
            return cached_data

        # Consultar MongoDB
        standings = await self.mongodb_client.get_standings(
            league_id=league_id, season=season
        )

        # Convertir a diccionarios
        result = [standing.model_dump(by_alias=False) for standing in standings]

        # Guardar en caché
        await self.memory_cache.set(
            cache_key, result, ttl=self.config.cache_ttl_standings
        )

        return result

    def _current_season(self) -> str:
        now = datetime.now()
        return str(now.year if now.month >= 8 else now.year - 1)

    async def cleanup(self) -> None:
        """
        Limpia los recursos utilizados por el servicio.
        """
        self.mongodb_client.close()
        await self.memory_cache.cleanup_expired()
