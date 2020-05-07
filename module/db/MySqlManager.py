
import mysql.connector as mysqlconn
import mysql.connector.pooling
import logging

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

    def initMySql(self, host, port, user, passwd, dbname, cbAndEvt):
        try:
            self.host = host
            self.port = port
            self.user = user
            self.passwd = passwd
            self.dbname = dbname
            self.cbAndEvt = cbAndEvt
            logging.info("{0}:{1} {2}, DB Name: {3}".format(host, port, user, dbname))
            dbconfig = {
                "database": dbname,
                "user": user,
                "password": passwd,
                "host": host,
                "port": port,
                "connect_timeout": 3000
            }            
            self.pool = mysqlconn.pooling.MySQLConnectionPool(pool_size=4, pool_name=self.DB_POOLNAME, **dbconfig)
            self.cbAndEvt.onEventDbConnect.fire(f"mysql connected {host}, {user}, {dbname}")
            return True
        except Exception as ex:
            exutil.printException()
            self.cbAndEvt.onEventDbDisconnect.fire(f"mysql disconnected {host}, {user}, {dbname}")
            return False

    def closeMySql(self):
        try:
            self.pool._remove_connections()
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

    def insertOne(self, query):
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            return True
        except Exception as ex:
            exutil.printException()
            self.cbAndEvt.onDbError.fire(str(ex))
            #if(self.cbAndEvt != None):
            #    self.cbAndEvt.on_disconnected("disconnected")
            return False

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
