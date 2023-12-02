#!/usr/bin/env python3
"""Writing strings to Redis"""
from typing import Any, Callable, Union
import redis
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Count how many times methods of a class is called"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Increment count each time method is called"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Cache store"""

    def __init__(self) -> None:
        """Initialize the cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store an item in the cache"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Any:
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
