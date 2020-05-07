from datetime import datetime, timedelta
from common.utils.CryptoHelper import CryptoHelper
from common.utils.StrUtils import StrUtils
import common.utils.keygen as keygen

class UserToken:

    EXPIRE_MINUTES = 60
    def create(self, scode, userId, userName, uuid, loginTokenId):
        #expireAt = datetime.now() + timedelta(days=self.EXPIRE_DAYS)
        startAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        tokenId = StrUtils.getSha256Uuid('tokenId:')
        token = CryptoHelper.enc(tokenId + chr(31) + loginTokenId + chr(31) + scode + chr(31) + userId + chr(31) + userName + chr(31) + uuid + chr(31) + startAt)
        
        return tokenId, token

    def parse(self, token):
        token = CryptoHelper.dec(token)
        token = token.split(chr(31), -1)
        if len(token) < 7:
            return None
        return {'tokenId':token[0], 'loginTokenId': token[1], 'scode': token[2], 'userId': token[3], 'userName': token[4], 'uuid': token[5], 'startAt': token[6]}

    def isExpired(self, startAt):
        now = datetime.now()
        startAt = datetime.strptime(startAt, '%Y-%m-%d %H:%M:%S')

        return now - timedelta(minutes=self.EXPIRE_MINUTES) > startAt
