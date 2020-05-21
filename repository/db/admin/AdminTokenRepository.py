from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime

from repository.db.DbRepository import DbRepository


class AdminTokenRepository(DbRepository):

    def upsert(self, userId, token, remoteIp):
        sql = f"INSERT INTO adminToken (userId, token, remoteIp) VALUES('{userId}', '{token}', '{remoteIp}') \
                ON DUPLICATE KEY UPDATE token='{token}', remoteIp='{remoteIp}', issuedAt=now()"
        return self.update(sql)

    def updateToken(self, userId, token):
        sql = f"UPDATE adminToken SET token='{token}', issuedAt=now() WHERE userId='{userId}'"
        return self.update(sql)


    def delete(self, userId):
        sql = f"DELETE FROM adminToken WHERE userId='{userId}'"
        return self.delete(sql)


    def getToken(self, userId):
        sql = f"SELECT * FROM adminToken WHERE userId='{userId}'"
        return self.getOne(sql)

    def updateLasttime(self, userId):
        sql = f"UPDATE adminToken SET issuedAt=now() WHERE userId='{userId}'"
        return self.update(sql)

    def isAvailableToken(self, userId, token):
        sql = f"SELECT * FROM adminToken WHERE userId='{userId}' AND token='{token}' ORDER BY issuedAt DESC LIMIT 1"
        return len(self.select(sql)) > 0

