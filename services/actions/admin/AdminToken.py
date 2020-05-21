from datetime import datetime, timedelta
import common.utils.CryptoHelper as CryptoHelper

class AdminToken:
    EXPIRE_DAYS = 30

    def createUser(self, userId, role, userName):
        expireDay = datetime.now() + timedelta(days=self.EXPIRE_DAYS)
        expireDayStr = expireDay.strftime('%Y-%m-%d %H:%M:%S')
        return CryptoHelper.encrypt(userId + chr(31) + role + chr(31) + userName + chr(31) + expireDayStr)

    def parseUser(self, token):
        token = CryptoHelper.decrypt(token)
        token = token.split(chr(31), -1)
        if len(token) < 4:
            return None
        return {'userId': token[0], 'role': token[1], 'userName':token[2], 'expireAt': token[3]}

    def createApp(self, appId, scode):
        return CryptoHelper.encrypt(appId + chr(31) + scode)

    def parseApp(self, token):
        token = CryptoHelper.decrypt(token)
        token = token.split(chr(31), -1)
        if len(token) < 2:
            return None, None
        appId = token[0]
        scode = token[1]
        return appId, scode


    def isExpired(self, expireDate):
        now = datetime.now()
        expire = datetime.strptime(expireDate, '%Y-%m-%d %H:%M:%S')

        return now - timedelta(days=self.EXPIRE_DAYS) > expire
