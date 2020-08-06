"""
Cache implementation.
Currently only two types of cache are allowed:
    * "none"    cache switched off
    * "redis"   use redis for cache

Configuration parameters:

    cache.type = redis | none
    cache.redis.db
    cache.redis.host
    cache.redis.port
"""

import os
import json
from config import CONFIG

_REDIS = None
if CONFIG['cache.type'] == 'redis':
    import redis
    _REDIS = redis.Redis(
        host=CONFIG['cache.redis.host'],
        port=CONFIG['cache.redis.port'],
        db=CONFIG['cache.redis.db'])

_REDIS_PREFIX = ''
if CONFIG.get("cache.redis.prefix", ""):
    _REDIS_PREFIX = CONFIG["cache.redis.prefix"] + ":"

def put(key, value):
    """
    Save `value` with `key`, and serialize it if needed
    """

    if _REDIS_PREFIX:
        key = _REDIS_PREFIX + key

    if CONFIG["cache.type"] == "redis" and _REDIS:
        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        _REDIS.set(key, value)

def get(key):
    """
    Read `value` by `key`, and deserialize it if needed
    """

    if _REDIS_PREFIX:
        key = _REDIS_PREFIX + key

    if CONFIG["cache.type"] == "redis" and _REDIS:
        value = _REDIS.get(key)
        try:
            value = json.loads(value)
        except (ValueError, TypeError):
            pass
        return value
    return None

def delete(key):
    """
    Remove `key` from the database
    """

    if _REDIS:
        if _REDIS_PREFIX:
            key = _REDIS_PREFIX + key

        _REDIS.delete(key)

    return None
