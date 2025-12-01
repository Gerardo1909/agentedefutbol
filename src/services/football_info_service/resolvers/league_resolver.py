"""
Resolver para ligas de fútbol.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from core.logging import football_resolver_logger

from services.football_info_service.resolvers.resolver import Resolver


class LeagueResolver(Resolver):
    """
    Resuelve nombres y aliases de ligas a sus IDs.
    """

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Inicializa el resolver de ligas.

        Args:
            data_dir: Directorio donde se encuentra leagues.json
        """
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data"

        self.leagues: Dict[str, int] = {}
        self.league_aliases: Dict[str, List[str]] = {}

        self._load_leagues(data_dir / "leagues.json")

    def _load_leagues(self, file_path: Path) -> None:
        """
        Carga ligas y aliases desde archivo JSON.

        Args:
            file_path: Ruta al archivo leagues.json
        """
        if not file_path.exists():
            football_resolver_logger.warning(
                f"Archivo de ligas no encontrado: {file_path}"
            )
            self.leagues = {}
            self.league_aliases = {}
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for league_name, league_data in data.items():
                    self.leagues[league_name] = league_data["id"]
                    self.league_aliases[league_name] = league_data.get("aliases", [])
            football_resolver_logger.info(
                f"Cargadas {len(self.leagues)} ligas desde {file_path}"
            )
        except (json.JSONDecodeError, IOError, KeyError) as e:
            football_resolver_logger.error(
                f"Error cargando ligas desde {file_path}: {e}"
            )
            self.leagues = {}
            self.league_aliases = {}

    def resolve(self, query: str, **kwargs) -> Optional[int]:
        """
        Resuelve el ID de una liga desde su nombre o alias.

        Args:
            query: Nombre o alias de la liga

        Returns:
            ID de la liga o None si no se encuentra
        """
        football_resolver_logger.debug(f"Intentando resolver liga: '{query}'")
        query_lower = query.lower().strip()

        # Búsqueda exacta por nombre
        for league_name, league_id in self.leagues.items():
            if league_name.lower() == query_lower:
                football_resolver_logger.info(
                    f"Liga resuelta por nombre exacto: '{query}' -> ID {league_id}"
                )
                return league_id

        # Búsqueda exacta por alias
        for league_name, league_id in self.leagues.items():
            aliases = self.league_aliases.get(league_name, [])
            if any(alias.lower() == query_lower for alias in aliases):
                football_resolver_logger.info(
                    f"Liga resuelta por alias exacto: '{query}' -> ID {league_id} ({league_name})"
                )
                return league_id

        # Búsqueda parcial por alias
        for league_name, league_id in self.leagues.items():
            aliases = self.league_aliases.get(league_name, [])
            if any(query_lower in alias.lower() for alias in aliases):
                football_resolver_logger.info(
                    f"Liga resuelta por alias parcial: '{query}' -> ID {league_id} ({league_name})"
                )
                return league_id

        football_resolver_logger.warning(f"No se pudo resolver liga: '{query}'")
        return None

    def get_name(self, entity_id: int, **kwargs) -> Optional[str]:
        """
        Obtiene el nombre oficial de una liga desde su ID.

        Args:
            entity_id: ID de la liga

        Returns:
            Nombre oficial de la liga o None si no se encuentra
        """
        football_resolver_logger.debug(f"Buscando nombre para liga ID: {entity_id}")
        for league_name, league_id in self.leagues.items():
            if league_id == entity_id:
                football_resolver_logger.debug(
                    f"Nombre encontrado: ID {entity_id} -> '{league_name}'"
                )
                return league_name
        football_resolver_logger.warning(
            f"No se encontró nombre para liga ID: {entity_id}"
        )
        return None

    def get_supported_leagues(self) -> List[str]:
        """
        Obtiene la lista de ligas soportadas.

        Returns:
            Lista de nombres de ligas
        """
        return list(self.leagues.keys())
