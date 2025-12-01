"""
Cliente para obtener información de fútbol desde MongoDB.
"""

from services.football_info_service.source_client.mongodb_client import MongoDBClient
from services.football_info_service.source_client.connection_pool import (
    MongoConnectionPool,
)

__all__ = ["MongoDBClient", "MongoConnectionPool"]
