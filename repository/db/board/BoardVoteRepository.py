from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class BoardVoteRepository(MultiDbRepository):


	def insert(self, scode, boardId,  userId,  userName,  expiredAt):
		expiredAtStr = datetime.strftime(expiredAt, "yyyy-MM-dd HH:mm:ss")
		sql = f"INSERT INTO vote (boardId, userId, userName, expiredAt) VALUES('{boardId}', '{userId}', '{userName}', '{expiredAtStr}')"
		return self.insertQuery(scode, sql)
	

	def updateExpireTime(self, scode, boardId,  userId,  expiredAt):
		expiredAtStr = datetime.strftime(expiredAt, "yyyy-MM-dd HH:mm:ss")
		sql = f"UPDATE vote SET expiredAt='{expiredAtStr}' WHERE boardId='{boardId}' AND userId='{userId}'"
		return self.updateQuery(scode, sql)	

	def updateClose(self, scode, boardId,  userId, closed):
		sql = f"UPDATE vote SET closed={closed} WHERE boardId='{boardId}' AND userId='{userId}'"
		return self.updateQuery(scode, sql)
	

	def delete(self, scode, boardId,  userId):
		sql = f"DELETE FROM vote WHERE boardId='{boardId}' AND userId='{userId}'"
		return self.deleteQuery(scode, sql)
	

	def getVoteInfo(self, scode, boardId):
		sql = f"SELECT * FROM vote WHERE boardId='{boardId}'"
		return self.selectQuery(scode, sql)
	

	def getVoteInfoList(self, scode, boardIds):
		ids = ','.join(["'" + str(id)+"'" for id in boardIds])
		sql = f"SELECT * FROM vote WHERE boardId IN ({ids})"
		return self.selectQuery(scode, sql)
	
	
	