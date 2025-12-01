"""
Clase base abstracta para resolvers.
"""

from abc import ABC, abstractmethod
from typing import Optional


class Resolver(ABC):
    """
    Clase base para todos los resolvers.
    Los resolvers traducen nombres/aliases a IDs de entidades.
    """

    @abstractmethod
    def resolve(self, query: str, **kwargs) -> Optional[int]:
        """
        Resuelve un nombre o alias a su ID correspondiente.

        Args:
            query: Nombre o alias a resolver
            **kwargs: Parámetros adicionales específicos del resolver

        Returns:
            ID de la entidad o None si no se encuentra
        """
        ...

    @abstractmethod
    def get_name(self, entity_id: int) -> Optional[str]:
        """
        Obtiene el nombre canónico de una entidad desde su ID.

        Args:
            entity_id: ID de la entidad

        Returns:
            Nombre de la entidad o None si no se encuentra
        """
        ...
