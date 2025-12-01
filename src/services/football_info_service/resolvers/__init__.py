"""
Módulo de resolvers para traducir nombres a IDs.
"""

from services.football_info_service.resolvers.league_resolver import LeagueResolver
from services.football_info_service.resolvers.team_resolver import TeamResolver

__all__ = ["LeagueResolver", "TeamResolver"]
