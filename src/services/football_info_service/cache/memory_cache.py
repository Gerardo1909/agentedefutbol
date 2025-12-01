"""
Implementación de caché en memoria con TTL.
"""

from datetime import datetime
from typing import Any, Optional

from core.logging import football_cache_logger
from services.football_info_service.models import CacheEntry


class MemoryCache:
    """
    Caché en memoria simple con soporte para TTL (Time To Live).
    """

    def __init__(self):
        """Inicializa el caché vacío."""
        self._cache: dict[str, CacheEntry] = {}
        self._stats = {"hits": 0, "misses": 0, "evictions": 0}

    async def get(self, key: str) -> Optional[Any]:
        """
        Obtiene un valor del caché.

        Args:
            key: Clave del caché

        Returns:
            Valor cacheado o None si no existe o expiró
        """
        entry = self._cache.get(key)

        if entry is None:
            self._stats["misses"] += 1
            football_cache_logger.debug(f"Cache MISS - Key: {key}")
            return None

        if entry.is_expired():
            del self._cache[key]
            self._stats["misses"] += 1
            self._stats["evictions"] += 1
            football_cache_logger.debug(f"Cache MISS - Key expirada: {key}")
            return None

        self._stats["hits"] += 1
        football_cache_logger.debug(f"Cache HIT - Key: {key}")
        return entry.data

    async def set(self, key: str, value: Any, ttl: int) -> None:
        """
        Guarda un valor en el caché con TTL.

        Args:
            key: Clave del caché
            value: Valor a cachear
            ttl: Time to live en segundos
        """
        entry = CacheEntry(data=value, cached_at=datetime.now(), ttl=ttl)
        self._cache[key] = entry
        football_cache_logger.debug(f"Cache SET - Key: {key}, TTL: {ttl}s")

    async def delete(self, key: str) -> bool:
        """
        Elimina una entrada del caché.

        Args:
            key: Clave a eliminar

        Returns:
            True si se eliminó, False si no existía
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    async def clear(self) -> None:
        """Limpia todo el caché."""
        self._cache.clear()
        self._stats["evictions"] += len(self._cache)

    async def cleanup_expired(self) -> int:
        """
        Limpia entradas expiradas del caché.

        Returns:
            Número de entradas eliminadas
        """
        expired_keys = [key for key, entry in self._cache.items() if entry.is_expired()]

        for key in expired_keys:
            del self._cache[key]

        self._stats["evictions"] += len(expired_keys)
        if expired_keys:
            football_cache_logger.info(f"Cache cleanup - Entradas expiradas eliminadas: {len(expired_keys)}")
        return len(expired_keys)

    def get_stats(self) -> dict[str, Any]:
        """
        Obtiene estadísticas del caché.

        Returns:
            Diccionario con estadísticas (tamaño, hits, misses, etc.)
        """
        total_requests = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total_requests if total_requests > 0 else 0.0

        return {
            "size": len(self._cache),
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "evictions": self._stats["evictions"],
            "hit_rate": round(hit_rate, 2),
            "total_requests": total_requests,
        }
