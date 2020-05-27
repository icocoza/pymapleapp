import os 
from module.db.MultiDbManager import MultiDbManager
import common.config.appconfig as appconfig
import common.utils.ExceptionUtil as exutil
import time, logging
import mysql.connector as mysqlconn
import mysql.connector.pooling
from common.inf.DbConnectionListener import DbConnectionListener
from common.utils.EventHook import EventHook

class MultiDbHelper(DbConnectionListener):

    _instance = None

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._getInstance
        return cls._instance

    def __init__(self):
        self.onEventDbConnect = EventHook()
        self.onEventDbConnect += self.onDbConnected
        self.onEventDbError = EventHook()
        self.onEventDbError += self.onDbError
        self.onEventDbDisconnect = EventHook()
        self.onEventDbDisconnect += self.onDbDisconnected

        self.databaseMaker = DatabaseMaker()
        
    def hasScode(self, scode):
        return MultiDbManager.instance().hasScode(scode)

    def createDatabaseWithDefault(self, scode):
        return self.createDatabase(scode, appconfig.dbhost, appconfig.dbport, appconfig.dbuser, appconfig.dbpassword)

    def createDatabase(self, scode, host, port, user, passwd):
        return self.databaseMaker.createDatabase(scode, host, port, user, passwd)

    def initMysqlWithDefault(self, scode):
        return self.initMySqlWithDatabase(scode, appconfig.dbhost, appconfig.dbport, appconfig.dbuser, appconfig.dbpassword, scode)

    def initMySqlWithDatabase(self, scode, host, port, user, passwd, dbname):
        return MultiDbManager.instance().addMySql(scode, host, port, user, passwd, dbname, self)

    def closeMySql(self, scode):
        MultiDbManager.instance().delMySql(scode)

    def restartMySql(self, scode, cbAndEvt):
        self.initMysqlWithDefault(scode, self)
        time.sleep(3)
        self.closeMySql(scode)

    def createTables(self, scode):
        for table in self.databaseMaker.tableQueries:
            MultiDbManager.instance().nonSelect(scode, table)
            
#/////////////EVENT///////////////////  
    def onDbConnected(self, status):
        logging.info(status)
        pass

    def onDbDisconnected(self, status):
        logging.error(status)
        pass
    
    def onDbError(self, status):  #db manager
        logging.error(status)
        pass


class DatabaseMaker:

    def __init__(self):
        self.__loadAppTableInfo()
        pass

    def createDatabase(self, scode, host, port, user, passwd):  #scode means database name
        try:
            logging.info("{0}:{1} {2}, DB Name: {3}".format(host, port, user, scode))
            dbconfig = {
                "user": user,
                "password": passwd,
                "host": host,
                "port": port,
                "connect_timeout": 3000
            }            
            pool = mysqlconn.pooling.MySQLConnectionPool(pool_size=2, pool_name='DBMAKER_POOL', **dbconfig)
            sql = f"CREATE DATABASE IF NOT EXISTS {scode} "
            conn = pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            pool._remove_connections()
            return True
        except Exception as ex:
            exutil.printException()
            return False

    def __loadAppTableInfo(self):
        sqlFile = os.getcwd() + "/resources/sql/app.sql"
        file = open(sqlFile,mode='r')
        filetext = file.read()
        file.close()
        self.tableQueries = filetext.split("\n\n", -1)
        pass
