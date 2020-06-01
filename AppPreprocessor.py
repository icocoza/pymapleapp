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
from services.actions.Action import Action
from services.worker.WorkerFactory import WorkerFactory

import common.utils.ExceptionUtil as exutil

REDIS_QUEUE_DATA = 'maple.collector'
REDIS_QUEUE_DATA_SERVER = 'maple.collector.server:'

class AppPreprocessor(DbConnectionListener):
    
    def __init__(self, serviceType, buildType):
        logging.info('buildType: '+buildType)
        self.threading = True

        self.workerFactory = WorkerFactory()
        #if buildType!='dev':
        RedisManager.instance().initRedisSentinel(appconfig.redis_host_port, appconfig.redis_master, appconfig.redis_password)
        #else:
        #    RedisManager.instance().initRedisSingle('127.0.0.1', 6379)

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
        logging.info('Connected: ' + dbName)
        if dbName is 'init':
            self.__initializeAdminDatabase()

    def onDbDisconnected(self, dbName):
        logging.info('Disconnected: ' + dbName)
        if dbName != 'init':
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
        logging.info(f'onRedisQueueData:\n{data}')
        jdata = json.loads(data)
        if 'server' not in jdata or 'sessionId' not in jdata:
            logging.error('Invalid Packet\n' + data)
            return
        result = None
        if 'stype' in jdata:
            worker = self.workerFactory.createFactory(jdata['stype'])
            if worker is None:
                result = Action().setOk('unknown', 'Not Implemented Stype')
            else:
                result = worker.workJson(jdata)
            logging.info(f'Result: {result}')
            result['sessionId'] = jdata['sessionId']
            jstr = json.dumps(result, default=self.outputDateTimeJSON) 
            RedisManager.instance().lpush(REDIS_QUEUE_DATA_SERVER+jdata['server'], jstr)
        else:
            logging.error(f'Unknown Servie Type {jdata}')

    def outputDateTimeJSON(self, obj):
        if isinstance(obj, datetime):
            if obj.utcoffset() is not None:
                obj = obj - obj.utcoffset()

            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return str(obj)

    def threadRedisQueueFunc(self): #Read Redis Queue
        queueCheckPointAt = datetime.now()
        while self.threading:
            try:
                # if queueCheckPointAt < datetime.now() - timedelta(seconds=10):
                #     RedisManager.instance().setTtl(REDIS_QUEUE_DATA + '.id:'+, 'queue', 10)
                #     queueCheckPointAt = datetime.now()

                data = RedisManager.instance().brPop(REDIS_QUEUE_DATA)
                if data == None:
                    continue
                data = data[1].decode('utf-8')
                logging.info(data)
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
 