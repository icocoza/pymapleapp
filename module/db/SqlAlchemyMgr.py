
from sqlalchemy import create_engine
import pymysql
import pandas as pd

import logging

class SqlAlchemyMgr:
    _instance = None
    DB_POOLNAME = '__HIVE__'

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
            config = f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{dbname}"
            self.sqlEngine       = create_engine(config, pool_recycle=3600)
            self.cbAndEvt = cbAndEvt
            return True
        except Exception as ex:
            logging.error(str(ex))
            self.cbAndEvt.onEventDbDisconnect.fire("failToInit")
            return False

    def closeMySql(self):
        try:
            self.sqlEngine.dispose()
        except Exception as ex:
            logging.error(str(ex))
    
    #https://www.pythonsheets.com/notes/python-sqlalchemy.html
    def select(self, query):                
        try:            
            conn = self.sqlEngine.connect()
            df = pd.read_sql(query, conn)
            #pd.set_option('display.expand_frame_repr', False)
            return df
        except Exception as ex:
            logging.error(ex)
            self.cbAndEvt.onEventDbError.fire("disconnected")
            return None
        finally:
            conn.close()

    def insertOne(self, query):
        try:
            conn = self.sqlEngine.connect()
            trans = conn.begin()
            conn.execute(query)
            trans.commit()            
            return True
        except Exception as ex:
            logging.error(ex)
            self.cbAndEvt.onEventDbError.fire("disconnected")
            return False
        finally:            
            conn.close()

    def insertQueries(self, queries):
        try:
            conn = self.sqlEngine.connect()
            trans = conn.begin()
            for query in queries:
                conn.execute(query)
            trans.commit()            
            return True
        except Exception as ex:
            logging.error(ex)
            self.cbAndEvt.onEventDbError.fire("disconnected")
            return False
        finally:
            conn.close()

    def updateOne(self, query):
        return self.insertOne(query)
    