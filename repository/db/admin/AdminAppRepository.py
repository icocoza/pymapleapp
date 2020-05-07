from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.DbRepository import DbRepository

class AdminAppRepository(DbRepository):
    
    def insertApp(self, appId, userId, scode, token, title, description, status):
        sql = f"INSERT INTO adminApp (appId, userId, scode, title, token, description, status) \
                VALUES('{appId}', '{userId}', '{scode}', '{title}', '{token}', '{description}', '{status}')"
        return self.insertQuery(sql)

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
        return self.selectQuery(sql)    

    def updateApp(self, userId, scode, title, description, status):
        sql = f"UPDATE adminApp SET title='{title}', description='{description}', status='{status}', statusAt=now() \
                WHERE userId='{userId}' AND scode='{scode}'"
        return self.updateQuery(sql)

    def updatePushInfo(self, userId, scode, fcmId, fcmKey):
        sql = f"UPDATE adminApp SET fcmId='{fcmId}', fcmKey='{fcmKey}', statusAt=now() WHERE userId='{userId}' AND scode='{scode}'"
        return self.updateQuery(sql)

    def updateStatus(self, userId, scode, status):
        sql = f"UPDATE adminApp SET status='{status}', statusAt=now() WHERE userId='{userId}' AND scode='{scode}'"
        return self.updateQuery(sql)

    def updateExternalDbInfo(self, userId, scode, dbHost, dbPort, dbOptions, dbUserId, dbPassword):
        sql = f"UPDATE adminApp SET dbHost='{dbHost}', dbPort='{dbPort}', dbOptions='{dbOptions}', dbUserId='{dbUserId}', dbPassword='{dbPassword}' \
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
        return len(self._selectToJson(self.selectQuery(sql))) > 0

