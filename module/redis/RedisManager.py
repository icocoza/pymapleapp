import logging
import redis
from redis.sentinel import Sentinel

class RedisManager:
    _instance = None

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._getInstance
        return cls._instance

    def initRedisSentinel(self, hostAndPort, masterName, passwd):
        hostPortList = self.__makeHostAndPortTuples(hostAndPort)

        self.sentinel = Sentinel(hostPortList)
        host, port = self.sentinel.discover_master(masterName)
        self.redis_client = redis.StrictRedis(host=host, port=port, password = None if passwd=='None' else passwd)
        pass

    def initRedisSingle(self, host, port):
        pool = redis.ConnectionPool(host=host, port=port, db=0)
        self.redis_client = redis.Redis(connection_pool=pool)
        pass

    def __makeHostAndPortTuples(self, hostAndPort):
        hostPortList = []
        csvList = hostAndPort.split(',', -1)
        for hostPort in csvList:
            hosts = hostPort.split(':', -1)
            hostPortList.append( (hosts[0], int(hosts[1])))

        return hostPortList

    def setTtl(self, key, value, seconds):
        self.redis_client.setex(key, seconds, value)

    def get(self, key):        
        return self.redis_client.get(key)

    def brPop(self, key):
        return self.redis_client.brpop(key, timeout=3)

    def lpush(self, key, value):
        return self.redis_client.lpush(key, value)