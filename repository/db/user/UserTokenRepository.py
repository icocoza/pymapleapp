from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class UserTokenRepository(MultiDbRepository):

	def getTokenByUserId(self, scode, userId):		
		sql = f"SELECT * FROM userToken WHERE userId='{userId}'"
		return super().selectOne(scode, sql)


	def getToken(self, scode, userId, uuid):
		sql = f"SELECT * FROM userToken WHERE userId='{userId}' and uuid='{uuid}'"
		return super().selectOne(scode, sql)


	def getTokenByUserTokenId(self, scode, userId, tokenId):
		sql = f"SELECT * FROM userToken WHERE userId='{userId}' AND tokenId='{tokenId}'"
		return super().selectOne(scode, sql)


	def insertToken(self, scode, userId, uuid, tokenId, token):
		return super().insert(qInsertToken(userId, uuid, tokenId, token, False))


	def qInsertToken(self, scode, userId, uuid, tokenId, token, enabled):
		return f"INSERT INTO userToken (userId, uuid, tokenId, token, enabled) VALUES('{userId}', '{uuid}', '{tokenId}', '{token}', {enabled})"

	def updateToken(self, scode, userId, uuid, tokenId, token, enabled):
		sql = f"UPDATE userToken SET token='{token}', tokenId='{tokenId}', enabled={enabled} WHERE userId='{userId}' AND uuid='{uuid}'"
		return super().update(scode, sql)


	def enableToken(self, scode, userId, tokenId, enabled):
		sql = f"UPDATE userToken SET enabled={enabled} WHERE userId='{userId}' AND tokenId='{tokenId}'"
		return super().update(scode, sql)


	def qDeleteTokenByUuid(self, scode, userId, uuid):
		return f"DELETE FROM userToken WHERE userId='{userId}' AND uuid='{uuid}'"


	def delete(self, scode, userId, tokenId):
		sql = f"DELETE FROM userToken WHERE userId='{userId}' AND token='{tokenId}'"
		return super().delete(scode, sql)


	def delete(self, scode, userId):
		sql = f"DELETE FROM userToken WHERE userId='{userId}'"
		return super().delete(scode, sql)
