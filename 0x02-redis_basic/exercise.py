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


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs for a particular function"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Store the history in redis cache"""
        input_list_key = "{}:inputs".format(method.__qualname__)
        self._redis.rpush(input_list_key, str(args))

        output = method(self, *args, **kwargs)
        output_list_key = "{}:outputs".format(method.__qualname__)
        self._redis.rpush(output_list_key, str(output))

        return output

    return wrapper


def replay(method: Callable) -> None:
    """Display the history of calls of a particular function"""
    _redis = redis.Redis()
    method_name = method.__qualname__
    inputs = _redis.lrange("{}:inputs".format(method_name), 0, -1)
    outputs = _redis.lrange("{}:outputs".format(method_name), 0, -1)

    print("{} was called {} times:".format(method_name, len(inputs)))
    for input, output in zip(inputs, outputs):
        print(
            "{}(*{}) -> {}".format(
                method_name, input.decode('utf-8'), output.decode('utf-8')
            )
        )


class Cache:
    """Cache store"""

    def __init__(self) -> None:
        """Initialize the cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
