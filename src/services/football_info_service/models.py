"""
Módulo de modelos Pydantic para el servicio de información de fútbol.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, ConfigDict


class Score(BaseModel):
    """
    Modelo para el resultado de un partido.
    """

    home: Optional[int] = None
    away: Optional[int] = None


class Match(BaseModel):
    """
    Modelo para un partido de fútbol.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    home_team: str
    away_team: str
    home_team_id: int
    away_team_id: int
    league: str
    league_id: int
    season: str
    date: datetime
    status: str  # "upcoming", "finished", "live", "postponed", "cancelled"
    score: Optional[Score] = None
    venue: Optional[str] = None
    round: Optional[str] = None


class Standing(BaseModel):
    """
    Modelo para la posición de un equipo en la tabla.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    team: str
    team_id: int
    league: str
    league_id: int
    season: str
    position: int
    points: int
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    goal_difference: int
    form: Optional[str] = None  # "WWDLL" - últimos 5 partidos


class CacheEntry(BaseModel):
    """
    Modelo para una entrada en caché con TTL.
    """

    data: Any
    cached_at: datetime
    ttl: int

    def is_expired(self) -> bool:
        """
        Verifica si la entrada en caché ha expirado basado en el TTL.
        """
        age = (datetime.now() - self.cached_at).total_seconds()
        return age > self.ttl


class MongoDBConfig(BaseModel):
    """
    Configuración para la conexión a MongoDB.
    """

    uri: str
    database_name: str
    max_pool_size: int = 10
    min_pool_size: int = 2
    max_idle_time_ms: int = 45000
    timeout_ms: int = 5000
