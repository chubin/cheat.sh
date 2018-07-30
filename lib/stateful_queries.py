"""
Support for the stateful queries
"""

import redis
from globals import REDISHOST

REDIS = redis.StrictRedis(host=REDISHOST, port=6379, db=1)

def save_query(client_id, query):
    """
    Save the last query `query` for the client `client_id`
    """
    REDIS.set("l:%s" % client_id, query)

def last_query(client_id):
    """
    Return the last query for the client `client_id`
    """
    return REDIS.get("l:%s" % client_id)
