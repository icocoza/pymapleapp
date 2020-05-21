from module.db.MySqlManager import MySqlManager
from module.db.SqlAlchemyMgr import SqlAlchemyMgr
import common.config.appconfig as appconfig

import time
class DbHelper:

    def initMysql(self, cbAndEvt):
        MySqlManager.instance().initMySql(appconfig.dbhost, appconfig.dbport, appconfig.dbuser, appconfig.dbpassword, cbAndEvt, poolCount=4)

    def initMysqlWithDefault(self, cbAndEvt):
        self.initMySqlWithDatabase(appconfig.dbhost, appconfig.dbport, appconfig.dbuser, appconfig.dbpassword, appconfig.dbname, cbAndEvt, poolCount=4)
        pass

    def initMySqlWithDatabase(self, host, port, user, passwd, dbname, cbAndEvt, poolCount):
        MySqlManager.instance().initMySqlWithDatabase(host, port, user, passwd, dbname, cbAndEvt, poolCount=poolCount)
        pass

    def closeMySql(self):
        MySqlManager.instance().closeMySql()

    def restartMySql(self, cbAndEvt):
        self.initMysqlWithDefault(cbAndEvt)
        time.sleep(3)
        self.closeMySql()

    def existDatabase(self, dbname):
        sql = f"SHOW DATABASES LIKE '{dbname}'"
        rows = MySqlManager.instance().select(sql)
        return rows is not None
    
    def createDatabase(self, dbname):
        sql = f"CREATE DATABASE {dbname}"
        return MySqlManager.instance().nonSelect(sql)
    
    def useDatabase(self, dbname):
        sql = f"USE {dbname}"
        return MySqlManager.instance().nonSelect(sql)

    def select(self, sql):
        return MySqlManager.instance().select(sql)

    def nonSelect(self, sql):
        return MySqlManager.instance().nonSelect(sql)

    def initSqlAlchemyWithDefault(self, cbAndEvt):
        self.initSqlAlchemy(appconfig.dbhost, appconfig.dbport, appconfig.dbuser, appconfig.dbpassword, appconfig.dbname, cbAndEvt)
        pass

    def initSqlAlchemy(self, host, port, user, passwd, dbname, cbAndEvt):
        SqlAlchemyMgr.instance().initMySqlWithDatabase(host, port, user, passwd, dbname, cbAndEvt)
        pass

    def closeSqlAlchemy(self):
        SqlAlchemyMgr.instance().closeMySql()

    def restartSqlAlchemy(self, cbAndEvt):
        self.initSqlAlchemyWithDefault(cbAndEvt)
        time.sleep(3)
        self.closeSqlAlchemy()