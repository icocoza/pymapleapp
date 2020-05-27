
import mysql.connector as mysqlconn
import mysql.connector.pooling
import logging
import common.utils.StrUtils as StrUtils

import common.utils.ExceptionUtil as exutil

class MySqlManager:
    _instance = None
    DB_POOLNAME = '_MYSQL_'

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._getInstance
        return cls._instance

    def __getDefaultConfig(self, host, port, user, passwd):
        config = {
            "user": user,
            "password": passwd,
            "host": host,
            "port": port,
            'connect_timeout': 3000,
            'time_zone': 'Asia/Seoul'
        }
        return config

    def initMySql(self, host, port, user, passwd, cbAndEvt, poolCount=1):
        try:
            self.host = host
            self.port = port
            self.user = user
            self.passwd = passwd
            self.cbAndEvt = cbAndEvt
            self.dbname = 'admin'
            logging.info("{0}:{1} {2}, DB Name: 'admin'".format(host, port, user))
            dbconfig = self.__getDefaultConfig(host, port, user, passwd)    
     
            self.pool = mysqlconn.pooling.MySQLConnectionPool(pool_size=poolCount, pool_name=self.DB_POOLNAME, **dbconfig)
            self.cbAndEvt.onEventDbConnect.fire('admin')
            return True
        except Exception as ex:
            exutil.printException()
            self.cbAndEvt.onEventDbDisconnect.fire('admin')
            return False

    def initMySqlWithDatabase(self, host, port, user, passwd, dbname, cbAndEvt, poolCount=4):
        try:
            self.host = host
            self.port = port
            self.user = user
            self.passwd = passwd
            self.dbname = dbname
            self.cbAndEvt = cbAndEvt
            logging.info("{0}:{1} {2}, DB Name: {3}".format(host, port, user, dbname))
            dbconfig = self.__getDefaultConfig(host, port, user, passwd)
            dbconfig['database'] = dbname
            self.pool = mysqlconn.pooling.MySQLConnectionPool(pool_size=poolCount, pool_name=self.DB_POOLNAME, **dbconfig)
            self.cbAndEvt.onEventDbConnect.fire(dbname)
            return True
        except Exception as ex:
            exutil.printException()
            self.cbAndEvt.onEventDbDisconnect.fire(dbname)
            return False

    def closeMySql(self):
        try:
            self.pool._remove_connections()
            self.cbAndEvt.onEventDbConnect.fire(self.dbname)
        except Exception as ex:
            exutil.printException()

    def select(self, query):                
        try:            
            conn = self.pool.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            records = cursor.fetchall()
            return records if len(records) > 0 else None
            #return [ dict(line) for line in [zip([ column[0] for column in cursor.description], row) for row in cursor.fetchall()] ]            
        except Exception as ex:
            exutil.printException()
            self.cbAndEvt.onDbError.fire(str(ex))
            #if(self.cbAndEvt != None):
            #    self.cbAndEvt.on_disconnected("disconnected")
            return None
        finally:
            if conn.is_connected() == True :
                cursor.close()
                conn.close()

    def execute(self, query, params):
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return True
        except Exception as ex:
            exutil.printException()
            self.cbAndEvt.onDbError.fire(str(ex))
            return False
        finally:
            if conn.is_connected() == True :
                cursor.close()
                conn.close()       

    # def insertOne(self, query):
    #     try:
    #         conn = self.pool.get_connection()
    #         cursor = conn.cursor()
    #         cursor.execute(query)
    #         conn.commit()
    #         return True
    #     except Exception as ex:
    #         exutil.printException()
    #         self.cbAndEvt.onDbError.fire(str(ex))
    #         #if(self.cbAndEvt != None):
    #         #    self.cbAndEvt.on_disconnected("disconnected")
    #         return False
    #     finally:
    #         if conn.is_connected() == True :
    #             cursor.close()
    #             conn.close()

    def multiQueries(self, queries):
        try:
            conn = self.pool.get_connection()
            conn.autocommit = False
            cursor = conn.cursor()
            for query in queries:
                cursor.execute(query)
            conn.commit()
            return True
        except Exception as ex:
            exutil.printException()
            self.cbAndEvt.onDbError.fire(str(ex))
            return False
        finally:
            if conn.is_connected() == True :
                cursor.close()
                conn.close()

    def insertQueries(self, queries):
        self.multiQueries(queries)
        
    def updateOne(self, query):
        return self.insertOne(query)
    
    def nonSelect(self, query):
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            return True
        except Exception as ex:
            exutil.printException()
            self.cbAndEvt.onDbError.fire(str(ex))
            return False
        finally:
            if conn.is_connected() == True :
                cursor.close()
                conn.close()
