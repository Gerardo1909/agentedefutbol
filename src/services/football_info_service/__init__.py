"""
Servicio de información de fútbol con integración a MongoDB.

Point of entry principal:
    from services.football_info_service import FootballInfoService
    
    service = FootballInfoService()
    fixtures = await service.get_team_upcoming_matches("Real Madrid")
"""

from .service import FootballInfoService
from .config import FootballInfoServiceConfig
from .exceptions import (
    FootballServiceError,
    SourceConnectionError,
    MongoDBConnectionError,
    MongoDBQueryError,
    DataNotFoundError,
    InvalidLeagueError,
    InvalidTeamError,
)

__all__ = [
    "FootballInfoService",
    "FootballInfoServiceConfig",
    "FootballServiceError",
    "SourceConnectionError",
    "MongoDBConnectionError",
    "MongoDBQueryError",
    "DataNotFoundError",
    "InvalidLeagueError",
    "InvalidTeamError",
]
