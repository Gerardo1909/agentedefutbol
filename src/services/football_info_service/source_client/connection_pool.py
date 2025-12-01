"""
Módulo para gestionar el pool de conexiones a MongoDB.
"""

from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database

from core.logging import football_info_getter_logger
from services.football_info_service.models import MongoDBConfig
from services.football_info_service.exceptions import MongoDBConnectionError


class MongoConnectionPool:
    """
    Gestiona el pool de conexiones a MongoDB.
    Implementa el patrón Singleton para reutilizar conexiones.
    """

    _instance: Optional["MongoConnectionPool"] = None
    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None

    def __new__(cls, config: Optional[MongoDBConfig] = None):
        """
        Implementa el patrón Singleton.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if config is not None:
                cls._instance._initialize(config)
        return cls._instance

    def _initialize(self, config: MongoDBConfig) -> None:
        """
        Inicializa la conexión a MongoDB.

        Args:
            config: Configuración de MongoDB
        """
        try:
            football_info_getter_logger.info(
                f"Inicializando conexión a MongoDB - Database: {config.database_name}"
            )

            self._client = MongoClient(
                config.uri,
                maxPoolSize=config.max_pool_size,
                minPoolSize=config.min_pool_size,
                maxIdleTimeMS=config.max_idle_time_ms,
                serverSelectionTimeoutMS=config.timeout_ms,
            )

            # Verificar conexión
            self._client.admin.command("ping")
            self._db = self._client[config.database_name]

            football_info_getter_logger.info(
                "Conexión a MongoDB establecida correctamente"
            )

        except Exception as e:
            football_info_getter_logger.error(
                f"Error al conectar a MongoDB: {str(e)}", exc_info=True
            )
            raise MongoDBConnectionError(
                f"No se pudo establecer conexión a MongoDB: {str(e)}", original_error=e
            )

    def get_database(self) -> Database:
        """
        Obtiene la base de datos MongoDB.

        Returns:
            Instancia de Database

        Raises:
            RuntimeError: Si la conexión no ha sido inicializada
        """
        if self._db is None:
            raise RuntimeError(
                "MongoDB connection not initialized. Call _initialize() first."
            )
        return self._db

    def close(self) -> None:
        """
        Cierra la conexión a MongoDB y libera recursos.
        """
        if self._client is not None:
            football_info_getter_logger.info("Cerrando conexión a MongoDB")
            self._client.close()
            self._client = None
            self._db = None
            MongoConnectionPool._instance = None

    def is_connected(self) -> bool:
        """
        Verifica si la conexión está activa.

        Returns:
            True si está conectado, False en caso contrario
        """
        if self._client is None:
            return False

        try:
            self._client.admin.command("ping")
            return True
        except Exception:
            return False
