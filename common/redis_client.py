'''
@author: lileilei
@file: redis_client.py
@time: 2018/9/19 10:49
'''
import redis
from config import redis_password, max_connec_redis


class ConRedisOper(object):
    _pool = None

    def __init__(self, host: str, port: int, db: int):
        self.host = host
        self.port = port
        self.db = db

    def connect(self):
        if ConRedisOper._pool is None:
            ConRedisOper._pool = redis.ConnectionPool(
                host=self.host, port=self.port,
                password=redis_password, db=self.db,
                max_connections=max_connec_redis)
        coon = redis.Redis(connection_pool=ConRedisOper._pool)
        return coon

    def sethash(self, key, value, time=None):
        if time:
            res = self.connect().setex(key, time, value)
        else:
            res = self.connect().set(key, value)
        return res

    def getset(self, key):
        res = self.connect().get(key)
        return res


def save_result(key, value):
    from config import redis_host, redis_port, redis_save_result_db, save_duration
    redis_cli = ConRedisOper(host=redis_host, port=redis_port, db=redis_save_result_db)
    redis_cli.sethash(str(key), str(value), save_duration)


def get_result(key):
    from config import redis_host, redis_port, redis_save_result_db
    redis_cli = ConRedisOper(host=redis_host, port=redis_port, db=redis_save_result_db)
    return redis_cli.getset(key)

# 向后兼容别名
save_reslut = save_result
get_reslut = get_result
