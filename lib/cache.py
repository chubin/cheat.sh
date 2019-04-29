import os
import json
import redis
from globals import REDISHOST

if os.environ.get('REDIS_HOST', '').lower() != 'none':
    _REDIS = redis.StrictRedis(host=REDISHOST, port=6379, db=0)
else:
    _REDIS = None

if os.environ.get('REDIS_PREFIX', ''):
    _REDIS_PREFIX = os.environ.get('REDIS_PREFIX', '') + ':'
else:
    _REDIS_PREFIX = ''

def put(key, value):
    """
    Save `value` with `key`, and serialize it if needed
    """

    if _REDIS_PREFIX:
        key = _REDIS_PREFIX + key

    if _REDIS:
        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        _REDIS.set(key, value)

def get(key):
    """
    Read `value` by `key`, and deserialize it if needed
    """

    if _REDIS_PREFIX:
        key = _REDIS_PREFIX + key

    if _REDIS:
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
