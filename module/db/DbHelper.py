from module.db.MySqlManager import MySqlManager
from module.db.SqlAlchemyMgr import SqlAlchemyMgr
import common.config.appconfig as appconfig

import time
class DbHelper:

    def initMysqlWithDefault(self, cbAndEvt):
        self.initMySql(appconfig.DB_HOST, appconfig.DB_PORT, appconfig.DB_USER, appconfig.DB_PASSWORD, appconfig.DB_NAME, cbAndEvt)
        pass

    def initMySql(self, host, port, user, passwd, dbname, cbAndEvt):
        MySqlManager.instance().initMySql(host, port, user, passwd, dbname, cbAndEvt)
        pass

    def closeMySql(self):
        MySqlManager.instance().closeMySql()

    def restartMySql(self, cbAndEvt):
        self.initMysqlWithDefault(cbAndEvt)
        time.sleep(3)
        self.closeMySql()

    
    def initSqlAlchemyWithDefault(self, cbAndEvt):
        self.initSqlAlchemy(appconfig.DB_HOST, appconfig.DB_PORT, appconfig.DB_USER, appconfig.DB_PASSWORD, appconfig.DB_NAME, cbAndEvt)
        pass

    def initSqlAlchemy(self, host, port, user, passwd, dbname, cbAndEvt):
        SqlAlchemyMgr.instance().initMySql(host, port, user, passwd, dbname, cbAndEvt)
        pass

    def closeSqlAlchemy(self):
        SqlAlchemyMgr.instance().closeMySql()

    def restartSqlAlchemy(self, cbAndEvt):
        self.initSqlAlchemyWithDefault(cbAndEvt)
        time.sleep(3)
        self.closeSqlAlchemy()