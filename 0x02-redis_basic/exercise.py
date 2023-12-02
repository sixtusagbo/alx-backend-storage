#!/usr/bin/env python3
"""Writing strings to Redis"""
from typing import Any, Callable, Union
import redis
import uuid


class Cache:
    """Cache store"""

    def __init__(self) -> None:
        """Initialize the cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store an item in the cache"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable) -> bytes:
        """Return data from the cache
        Uses the callable to convert the data to a specific desired format
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return data if fn is None else fn(data)

    def get_str(self, key: str) -> str:
        """Automatically parameterize `Cache.get`
        with str conversion function
        """
        return self.get(key, str)

    def get_int(self, key: int) -> int:
        """Automatically parameterize `Cache.get`
        with int conversion function
        """
        return self.get(key, int)
