"""
Cliente para obtener información de fútbol desde MongoDB.
"""

from datetime import datetime
from typing import List, Optional

from pymongo.database import Database

from core.logging import football_info_getter_logger
from services.football_info_service.models import Match, Standing, MongoDBConfig
from services.football_info_service.source_client.connection_pool import (
    MongoConnectionPool,
)
from services.football_info_service.exceptions import (
    MongoDBConnectionError,
    MongoDBQueryError,
)


class MongoDBClient:
    """
    Cliente para obtener información de fútbol desde MongoDB.
    """

    def __init__(self, config: Optional[MongoDBConfig] = None):
        """
        Inicializa el cliente MongoDB.

        Args:
            config: Configuración de MongoDB (opcional)
        """
        self.config = config
        self._pool: Optional[MongoConnectionPool] = None
        self._db: Optional[Database] = None

        if config:
            self._initialize_connection()

    def _initialize_connection(self) -> None:
        """
        Inicializa la conexión al pool de MongoDB.
        """
        if self.config is None:
            raise ValueError("MongoDB config is required for initialization")

        self._pool = MongoConnectionPool(self.config)
        self._db = self._pool.get_database()

    def _get_db(self) -> Database:
        """
        Obtiene la base de datos MongoDB.

        Returns:
            Instancia de Database

        Raises:
            RuntimeError: Si la conexión no está inicializada
        """
        if self._db is None:
            raise RuntimeError(
                "MongoDB client not initialized. Provide config during initialization."
            )
        return self._db

    async def get_upcoming_fixtures(
        self,
        league_id: Optional[int] = None,
        team_id: Optional[int] = None,
        limit: int = 5,
    ) -> List[Match]:
        """
        Obtiene fixtures (partidos) próximos.

        Args:
            league_id: ID de la liga (opcional)
            team_id: ID del equipo (opcional)
            limit: Número máximo de partidos a retornar

        Returns:
            Lista de partidos próximos
        """
        try:
            db = self._get_db()
            collection = db.matches

            # Construir query
            query: dict = {"status": "upcoming", "date": {"$gte": datetime.now()}}

            if league_id is not None:
                query["league_id"] = league_id

            if team_id is not None:
                query["$or"] = [
                    {"home_team_id": team_id},
                    {"away_team_id": team_id},
                ]

            football_info_getter_logger.info(
                f"Consultando fixtures próximos - Query: {query}, Limit: {limit}"
            )

            # Ejecutar query
            cursor = collection.find(query).sort("date", 1).limit(limit)
            matches = [Match(**doc) for doc in cursor]

            football_info_getter_logger.info(
                f"Fixtures próximos encontrados: {len(matches)}"
            )

            return matches

        except MongoDBConnectionError:
            raise
        except Exception as e:
            football_info_getter_logger.error(
                f"Error al obtener fixtures próximos: {str(e)}", exc_info=True
            )
            raise MongoDBQueryError(
                f"Error al consultar fixtures próximos: {str(e)}", query=query
            )

    async def get_past_fixtures(
        self,
        league_id: Optional[int] = None,
        team_id: Optional[int] = None,
        limit: int = 5,
    ) -> List[Match]:
        """
        Obtiene fixtures (partidos) pasados.

        Args:
            league_id: ID de la liga (opcional)
            team_id: ID del equipo (opcional)
            limit: Número máximo de partidos a retornar

        Returns:
            Lista de partidos pasados
        """
        try:
            db = self._get_db()
            collection = db.matches

            # Construir query
            query: dict = {"status": "finished", "date": {"$lt": datetime.now()}}

            if league_id is not None:
                query["league_id"] = league_id

            if team_id is not None:
                query["$or"] = [
                    {"home_team_id": team_id},
                    {"away_team_id": team_id},
                ]

            football_info_getter_logger.info(
                f"Consultando fixtures pasados - Query: {query}, Limit: {limit}"
            )

            # Ejecutar query (ordenar por fecha descendente para obtener los más recientes)
            cursor = collection.find(query).sort("date", -1).limit(limit)
            matches = [Match(**doc) for doc in cursor]

            football_info_getter_logger.info(
                f"Fixtures pasados encontrados: {len(matches)}"
            )

            return matches

        except MongoDBConnectionError:
            raise
        except Exception as e:
            football_info_getter_logger.error(
                f"Error al obtener fixtures pasados: {str(e)}", exc_info=True
            )
            raise MongoDBQueryError(
                f"Error al consultar fixtures pasados: {str(e)}", query=query
            )

    async def get_standings(
        self, league_id: int, season: Optional[str] = None
    ) -> List[Standing]:
        """
        Obtiene la tabla de posiciones para una liga y temporada.

        Args:
            league_id: ID de la liga
            season: Temporada (ej: "2025", si no se proporciona usa la actual)

        Returns:
            Lista de posiciones ordenadas
        """
        try:
            db = self._get_db()
            collection = db.standings

            # Si no se proporciona temporada, usar la actual
            if season is None:
                season = str(datetime.now().year)

            query = {"league_id": league_id, "season": season}

            football_info_getter_logger.info(
                f"Consultando tabla de posiciones - Query: {query}"
            )

            # Ejecutar query y ordenar por posición
            cursor = collection.find(query).sort("position", 1)
            standings = [Standing(**doc) for doc in cursor]

            football_info_getter_logger.info(
                f"Posiciones encontradas: {len(standings)}"
            )

            return standings

        except MongoDBConnectionError:
            raise
        except Exception as e:
            football_info_getter_logger.error(
                f"Error al obtener tabla de posiciones: {str(e)}", exc_info=True
            )
            raise MongoDBQueryError(
                f"Error al consultar tabla de posiciones: {str(e)}", query=query
            )

    def close(self) -> None:
        """
        Cierra la conexión con MongoDB.
        """
        if self._pool:
            self._pool.close()
            self._pool = None
            self._db = None
