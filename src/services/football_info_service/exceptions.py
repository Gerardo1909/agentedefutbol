"""
Excepciones personalizadas para el servicio de información de fútbol.
"""

from typing import Optional


class FootballServiceError(Exception):
    """Excepción base para errores del servicio."""


class SourceConnectionError(FootballServiceError):
    """Error de conexión con la fuente de datos (genérico)."""


class MongoDBConnectionError(SourceConnectionError):
    """Error específico de conexión a MongoDB."""

    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.original_error = original_error


class MongoDBQueryError(FootballServiceError):
    """Error al ejecutar una consulta en MongoDB."""

    def __init__(self, message: str, query: Optional[dict] = None):
        super().__init__(message)
        self.query = query


class DataNotFoundError(FootballServiceError):
    """No se encontraron datos para la búsqueda."""


class InvalidLeagueError(FootballServiceError):
    """Liga no soportada o inválida."""


class InvalidTeamError(FootballServiceError):
    """Equipo no encontrado o inválido."""
