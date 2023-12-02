#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
import uuid


class Cache:
    """Cache store"""

    def __init__(self):
        """Initialize the cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: str | bytes | int | float):
        """Store an item in the cache"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
