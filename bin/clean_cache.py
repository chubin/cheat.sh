import sys
import redis
REDIS = redis.StrictRedis(host='localhost', port=6379, db=0)

for key in sys.argv[1:]:
    REDIS.delete(key)

