from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.DbRepository import DbRepository

class AdminAppRepository(DbRepository):
    
    def insertApp(self, appId, userId, scode, token, title, description, status):
        params = (appId, userId, scode, title, token, description, status)
        sql = f"INSERT INTO adminApp (appId, userId, scode, title, token, description, status) \
                VALUES(%s, %s, %s, %s, %s, %s, %s)"
        return self.execute(sql, params)

    def getAppByAppId(self, appId):
        sql = f"SELECT * FROM adminApp WHERE appId='{appId}'"
        return self.selectOne(sql)

    def getAppByUid(self, userId, scode):
        sql = f"SELECT * FROM adminApp WHERE userId='{userId}' AND scode='{scode}'"
        return self.selectOne(sql)    

    def getAppList(self, userId):
        sql = f"SELECT * FROM adminApp WHERE userId='{userId}'"
        return self.selectQuery(sql)    

    def getAppByScode(self, scode):
        sql = f"SELECT * FROM adminApp WHERE scode='{scode}'"
        result = self.selectQuery(sql)
        return None if result is None else result[0]

    def updateApp(self, userId, scode, title, description, status):
        params = (title, description, status, userId, scode)
        sql = f"UPDATE adminApp SET title=%s, description=%s, status=%s, statusAt=now() \
                WHERE userId=%s AND scode=%s"
        return self.execute(sql, params)

    def updatePushInfo(self, userId, scode, fcmId, fcmKey):
        params = (fcmId, fcmKey, userId, scode)
        sql = f"UPDATE adminApp SET fcmId=%s, fcmKey=%s, statusAt=now() WHERE userId=%s AND scode=%s"
        return self.execute(sql, params)

    def updateStatus(self, userId, scode, status):
        sql = f"UPDATE adminApp SET status='{status}', statusAt=now() WHERE userId='{userId}' AND scode='{scode}'"
        return self.updateQuery(sql)

    def updateExternalDbInfo(self, userId, scode, dbHost, dbPort, dbUser, dbPassword):
        sql = f"UPDATE adminApp SET dbHost='{dbHost}', dbPort='{dbPort}', dbUser='{dbUser}', dbPassword='{dbPassword}' \
                WHERE userId='{userId}' AND scode='{scode}'"
        return self.updateQuery(sql)

    def getList(self, status, offset, count):
        sql = f"SELECT * FROM adminApp ORDER BY statusAt DESC LIMIT {offset}, {count}"
        if('all' != status):
            sql = f"SELECT * FROM adminApp WHERE status='{status}' ORDER BY statusAt DESC LIMIT {offset}, {count})"
        return self.selectQuery(sql)

    def getList(self, userId, status, offset, count):
        sql = f"SELECT * FROM adminApp WHERE userId='{userId}' ORDER BY statusAt DESC LIMIT {offset}, {count}"
        if('all' != status):
            sql = f"SELECT * FROM adminApp WHERE userId='{userId}' AND status='{status}' ORDER BY statusAt DESC LIMIT {offset}, {count}"
        return self.selectQuery(sql)

    def getAppCount(self, userId, status):
        if('all' != status):
            return self.count(f"SELECT COUNT(*) FROM adminApp WHERE userId='{userId}'")
        return self.count(f"SELECT COUNT(*) FROM adminApp WHERE userId='{userId}' AND status='{status}'")

    def hasSCode(self, scode):
        sql = f"SELECT * FROM adminApp WHERE scode='{scode}'"
        return self.selectQuery(sql) is not None

