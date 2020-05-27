
from module.db.MySqlManager import MySqlManager
import common.config.appconfig as appconfig

class MultiDbManager:
    _instance = None
    DB_POOLNAME = '_DBMANAGER_'

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._getInstance
        return cls._instance

    dbManagerMap = {}
    
    def addMySql(self, scode, host, port, user, passwd, dbname, cbAndEvt):
        dbManager = MySqlManager()
        if dbManager.initMySqlWithDatabase(host, port, user, passwd, dbname, cbAndEvt) == True:
            self.dbManagerMap[scode] = dbManager
            return True
        return False

    def hasScode(self, scode):
        return scode in self.dbManagerMap
        
    def addMysqlWithDefault(self, cbAndEvt):
        dbManager = MySqlManager()
        if dbManager.initMySqlWithDatabase(appconfig.dbhost, appconfig.dbport, appconfig.dbuser, appconfig.dbpassword, appconfig.dbname, cbAndEvt) == True:
            self.dbManagerMap[scode] = dbManager
            return True
        return False

    def delMySql(self, scode):
        if scode not in self.dbManagerMap:
            return False
        self.dbManagerMap[scode].closeMySql()
        return True

    def select(self, scode, query):
        if scode not in self.dbManagerMap:
            return []
        return self.dbManagerMap[scode].select(query)
    
    def insert(self, scode, query):
        if scode not in self.dbManagerMap:
            return False
        return self.dbManagerMap[scode].insertOne(query)

    def insertMany(self, scode, queries):
        if scode not in self.dbManagerMap:
            return False
        return self.dbManagerMap[scode].insertQueries(queries)

    def multiQueries(self, scode, queries):
        if scode not in self.dbManagerMap:
            return False
        return self.dbManagerMap[scode].multiQueries(queries)

    def update(self, scode, query):
        if scode not in self.dbManagerMap:
            return False
        return self.dbManagerMap[scode].updateOne(query)
    
    def delete(self, scode, query):
        if scode not in self.dbManagerMap:
            return False
        return self.dbManagerMap[scode].updateOne(query)

    def nonSelect(self, scode, query):
        if scode not in self.dbManagerMap:
            return False
        return self.dbManagerMap[scode].nonSelect(query)
