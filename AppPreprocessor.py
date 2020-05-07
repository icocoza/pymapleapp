#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import time, logging, threading
import numpy, json
from datetime import datetime, timedelta

from common.inf.DbConnectionListener import DbConnectionListener
from common.utils.EventHook import EventHook
import common.config.appconfig as appconfig
import common.const.unit_constant as unitConst

from module.db.MySqlManager import MySqlManager
from module.db.DbHelper import DbHelper
from module.redis.RedisManager import RedisManager

from services.worker.WorkerFactory import WorkerFactory

import common.utils.ExceptionUtil as exutil

APP_QUEUE_DATA = 'app.queue.data'
class AppProcessor(DbConnectionListener):
    
    def __init__(self):
        self.threading = True

        self.onEventDbConnect = EventHook()
        self.onEventDbConnect += self.onDbConnected
        self.onEventDbError = EventHook()
        self.onEventDbError += self.onDbError
        self.onEventDbDisconnect = EventHook()
        self.onEventDbDisconnect += self.onDbDisconnected
        DbHelper().initMysqlWithDefault(self)

        RedisManager.instance().initRedisSentinel(appconfig.redis_host_port, appconfig.redis_master, appconfig.redis_password)

        self.workerFactory = WorkerFactory()
        pass
    
    def start(self):
        self.redisQueueThread = threading.Thread(target=self.threadRedisQueueFunc)
        self.redisQueueThread.start()

    def stop(self):
        self.redisQueueThread.stop()
        self.threading = False

    def onRedisQueueData(self, data):
        jdata = json.loads(data)
        if 'stype' in jdata:
            worker = self.workerFactory(jdata['stype'])
            #worker...
        else:
            logging.error(f'Unknown Servie Type {jdata}')

    def onDbConnected(self, status):        
        pass

    def onDbDisconnected(self, status):
        logging.error(status)
        time.sleep(3)
        if status == 'mysql':
            DbHelper().initMysqlWithDefault(self)
        pass
    
    def onDbError(self, status):  #db manager
        logging.error(status)
        pass

    def threadRedisQueueFunc(self): #Read Redis Queue
        queueCheckPointAt = datetime.now()
        while self.threading:
            try:
                if queueCheckPointAt < datetime.now() - timedelta(seconds=5):
                    RedisManager.instance().setTtl('iot.sensor.data.queue', 'queue', 10)
                    queueCheckPointAt = datetime.now()

                data = RedisManager.instance().brPop(APP_QUEUE_DATA)
                if data == None:
                    time.sleep(3)
                    continue
                data = data[1].decode('utf-8')
                self.onRedisQueueData(data)
            except Exception as ex:
                exutil.PrintException()
                time.sleep(3)            