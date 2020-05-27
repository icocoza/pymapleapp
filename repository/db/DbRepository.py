from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from module.db.MySqlManager import MySqlManager

class DbRepository:

    def selectOne(self, sql):
        result = MySqlManager.instance().select(sql)
        if result is None or len(result) < 1:
            return None
        return result[0]
        
    def selectQuery(self, sql):
        return MySqlManager.instance().select(sql)

    def updateQuery(self, sql):
        return MySqlManager.instance().updateOne(sql)

    def deleteQuery(self, sql):
        return MySqlManager.instance().updateOne(sql)

    def insertQuery(self, sql):
        return MySqlManager.instance().insertOne(sql)

    def upsertQueries(self, queries):
        return MySqlManager.instance().insertQueries(queries)

    def count(self, sql):
        return len(MySqlManager.instance().select(sql))

    def exist(self, sql):
        return count(sql) > 0

    def select(self, sql):
        return MySqlManager.instance().select(sql)

    def update(self, sql):
        return MySqlManager.instance().updateOne(sql)

    def delete(self, sql):
        return MySqlManager.instance().updateOne(sql)

    def insert(self, sql):
        return MySqlManager.instance().insertOne(sql)

    def execute(self, sql, params):
        return MySqlManager.instance().execute(sql, params)