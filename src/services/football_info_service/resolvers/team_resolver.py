"""
Resolver para equipos de fútbol.
"""

import json
from pathlib import Path
from typing import Dict, Optional
from core.logging import football_resolver_logger

from services.football_info_service.resolvers.resolver import Resolver


class TeamResolver(Resolver):
    """
    Resuelve nombres de equipos a sus IDs.
    """

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Inicializa el resolver de equipos.

        Args:
            data_dir: Directorio donde se encuentra teams.json
        """
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data"

        self.teams: Dict[str, int] = {}
        self._load_teams(data_dir / "teams.json")

    def _load_teams(self, file_path: Path) -> None:
        """
        Carga equipos desde archivo JSON.

        Args:
            file_path: Ruta al archivo teams.json
        """
        if not file_path.exists():
            football_resolver_logger.warning(
                f"Archivo de equipos no encontrado: {file_path}"
            )
            self.teams = {}
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.teams = json.load(f)
            football_resolver_logger.info(
                f"Cargados {len(self.teams)} equipos desde {file_path}"
            )
        except (json.JSONDecodeError, IOError) as e:
            football_resolver_logger.error(
                f"Error cargando equipos desde {file_path}: {e}"
            )
            self.teams = {}

    def resolve(
        self, query: str, league_id: Optional[int] = None, **kwargs
    ) -> Optional[int]:
        """
        Resuelve el ID de un equipo desde su nombre.

        Args:
            query: Nombre del equipo
            league_id: ID de la liga (opcional, para filtrar búsqueda)

        Returns:
            ID del equipo o None si no se encuentra
        """
        football_resolver_logger.debug(
            f"Intentando resolver equipo: '{query}'{f' (liga ID: {league_id})' if league_id else ''}"
        )
        # TODO: En futuras versiones, filtrar por league_id si es necesario
        _ = league_id

        query_lower = query.lower().strip()

        # Búsqueda exacta
        for team_name, team_id in self.teams.items():
            if team_name.lower() == query_lower:
                football_resolver_logger.info(
                    f"Equipo resuelto por nombre exacto: '{query}' -> ID {team_id}"
                )
                return team_id

        # Búsqueda parcial
        for team_name, team_id in self.teams.items():
            if query_lower in team_name.lower():
                football_resolver_logger.info(
                    f"Equipo resuelto por nombre parcial: '{query}' -> ID {team_id} ({team_name})"
                )
                return team_id

        football_resolver_logger.warning(f"No se pudo resolver equipo: '{query}'")
        return None

    def get_name(self, entity_id: int, **kwargs) -> Optional[str]:
        """
        Obtiene el nombre oficial de un equipo desde su ID.

        Args:
            entity_id: ID del equipo

        Returns:
            Nombre oficial del equipo o None si no se encuentra
        """
        football_resolver_logger.debug(f"Buscando nombre para equipo ID: {entity_id}")
        for team_name, team_id in self.teams.items():
            if team_id == entity_id:
                football_resolver_logger.debug(
                    f"Nombre encontrado: ID {entity_id} -> '{team_name}'"
                )
                return team_name
        football_resolver_logger.warning(
            f"No se encontró nombre para equipo ID: {entity_id}"
        )
        return None
