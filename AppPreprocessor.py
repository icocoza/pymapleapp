#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os, time, logging, threading
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

REDIS_QUEUE_DATA = 'maple.collector'
REDIS_QUEUE_DATA_SERVER = 'maple.collector.server:'

class AppPreprocessor(DbConnectionListener):
    
    def __init__(self, serviceType, buildType):
        self.threading = True

        self.workerFactory = WorkerFactory()
        if buildType!='dev':
            RedisManager.instance().initRedisSentinel(appconfig.redis_host_port, appconfig.redis_master, appconfig.redis_password)
        else:
            RedisManager.instance().initRedisSingle('127.0.0.1', 6379)

        self.onEventDbConnect = EventHook()
        self.onEventDbConnect += self.onDbConnected
        self.onEventDbError = EventHook()
        self.onEventDbError += self.onDbError
        self.onEventDbDisconnect = EventHook()
        self.onEventDbDisconnect += self.onDbDisconnected

        self.dbHelper = DbHelper()
        self.dbHelper.initMysql(self)

        pass
    
    def onDbConnected(self, dbName):
        if dbName is 'admin':
            self.__initializeAdminDatabase()
        logging.info(dbName)

    def onDbDisconnected(self, dbName):
        logging.info('Disconnected: ' + dbName)
        if dbName != 'admin':
            time.sleep(3)
            self.dbHelper.initMysqlWithDefault(self)
    
    def onDbError(self, dbName):  #db manager
        logging.info('Error: ' + dbName)

    def start(self):
        self.redisQueueThread = threading.Thread(target=self.threadRedisQueueFunc)
        self.redisQueueThread.start()

    def stop(self):
        self.redisQueueThread.stop()
        self.threading = False

    def onRedisQueueData(self, data):
        jdata = json.loads(data)
        if 'server' not in jdata or 'sessionId' not in jdata:
            logging.error('Invalid Packet\n' + data)
            return
        if 'stype' in jdata:
            worker = self.workerFactory.createFactory(jdata['stype'])
            result = worker.workJson(jdata)
            result['sessionId'] = jdata['sessionId']
            RedisManager.instance().lpush(REDIS_QUEUE_DATA_SERVER+jdata['server'], str(result))
        else:
            logging.error(f'Unknown Servie Type {jdata}')

    def threadRedisQueueFunc(self): #Read Redis Queue
        queueCheckPointAt = datetime.now()
        while self.threading:
            try:
                # if queueCheckPointAt < datetime.now() - timedelta(seconds=10):
                #     RedisManager.instance().setTtl(REDIS_QUEUE_DATA + '.id:'+, 'queue', 10)
                #     queueCheckPointAt = datetime.now()

                data = RedisManager.instance().brPop(REDIS_QUEUE_DATA)
                if data == None:
                    time.sleep(3)
                    continue
                data = data[1].decode('utf-8')
                self.onRedisQueueData(data)
            except Exception as ex:
                exutil.printException()
                time.sleep(3)            

    def __initializeAdminDatabase(self):
        if self.dbHelper.existDatabase(appconfig.dbname) == False:
            if self.dbHelper.createDatabase(appconfig.dbname) == True:
                #self.dbHelper.useDatabase(appconfig.dbname)
                self.__createAdminTables()
        self.dbHelper.closeMySql()
        self.dbHelper.initMysqlWithDefault(self) #connect to admin database


    def __createAdminTables(self):
        sqlFile = os.getcwd() + "/resources/sql/admin.sql"
        file = open(sqlFile,mode='r')
        filetext = file.read()
        file.close()
        tableQueries = filetext.split("\n\n", -1)

        for table in tableQueries:
            self.dbHelper.nonSelect(table)
        pass
 