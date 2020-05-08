'''
@author: lileilei
@file: packageredis.py
@time: 2018/9/19 10:49
'''
import redis
from config import redis_password, max_connec_redis


class ConRedisOper(object):
    def __init__(self, host: int, port: int, db: int):
        self.host = host
        self.port = port
        self.db = db

    def connect(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port, password=redis_password, db=self.db,
                                    max_connections=max_connec_redis)
        coon = redis.Redis(connection_pool=pool)
        return coon

    def sethase(self, key, value, time=None):
        if time:
            res = self.connect().setex(key, value, time)
        else:
            res = self.connect().set(key, value)
        return res

    def getset(self, key):
        res = self.connect().get(key)
        return res
