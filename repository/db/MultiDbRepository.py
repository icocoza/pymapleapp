from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from module.db.MultiDbManager import MultiDbManager

class MultiDbRepository:

    def selectOne(self, scode, sql):
        result = MultiDbManager.instance().select(scode, sql)
        if result is None:
            return None
        return result[0]

    def selectQuery(self, scode, sql):
        return MultiDbManager.instance().select(scode, sql)

    def updateQuery(self, scode, sql):
        return MultiDbManager.instance().update(scode, sql)

    def deleteQuery(self, scode, sql):
        return MultiDbManager.instance().update(scode, sql)

    def insertQuery(self, scode, sql):
        return MultiDbManager.instance().insert(scode, sql)

    def upsertQueries(self, scode, queries):
        return MultiDbManager.instance().insertQueries(scode, queries)

    def multiQueries(self, scode, queries):
        return MultiDbManager.instance().multiQueries(scode, queries)

    def count(self, scode, sql):
        return len(MultiDbManager.instance().select(scode, sql))

    def exist(self, scode, sql):
        return count(scode, sql) > 0

    def select(self, scode, sql):
        return MultiDbManager.instance().select(scode, sql)

    def update(self, scode, sql):
        return MultiDbManager.instance().update(scode, sql)

    def delete(self, scode, sql):
        return MultiDbManager.instance().update(scode, sql)

    def insert(self, scode, sql):
        return MultiDbManager.instance().insert(scode, sql)

    def execute(self, scode, sql, params):
        return MultiDbManager.instance().execute(scode, sql, params)
