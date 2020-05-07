from datetime import datetime, timedelta
from common.utils.CryptoHelper import CryptoHelper
from common.utils.StrUtils import StrUtils
import common.utils.keygen as keygen

class UserToken:
    EXPIRE_DAYS = 90

    def create(self, scode, userId, uuid, authType):
        expireAt = datetime.now() + timedelta(days=self.EXPIRE_DAYS)
        expireAt = expireAt.strftime('%Y-%m-%d %H:%M:%S')

        tokenId = StrUtils.getSha256Uuid('tokenId:')
        token = CryptoHelper.enc(scode + chr(31) + userId + chr(31) + uuid + chr(31) + authType + chr(31) + expireAt) + chr(31) + str(int(float(datetime.now())*1000))
        
        return tokenId, token

    def parse(self, token):
        token = CryptoHelper.dec(token)
        token = token.split(chr(31), -1)
        if len(token) < 5:
            return None
        return {'scode': token[0], 'userId': token[1], 'uuid': token[2], 'authType':token[3], 'expireAt': token[4]}

    def isExpired(self, expireAt): #for loginToken
        now = datetime.now()
        expire = datetime.strptime(expireAt, '%Y-%m-%d %H:%M:%S')

        return now - timedelta(days=self.EXPIRE_DAYS) > expire

