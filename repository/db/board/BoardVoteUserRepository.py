from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class BoardVoteUserRepository(MultiDbRepository):

	def insert(self, scode, userId, boardId, voteItemId):
		sql = f"INSERT INTO voteUser (boardId, userId, voteItemId) VALUES('{boardId}','{userId}','{voteItemId}')"
		return super().insertQuery(scode, sql)


	def updateSelectItem(self, scode, userId, boardId, voteItemId):
		sql = f"UPDATE voteUser SET voteItemId='{voteItemId}', votedAt=NOW() WHERE userId='{userId}' AND boardId='{boardId}'"
		return super().updateQuery(scode, sql)


	def delete(self, scode, userId, boardId):
		sql = f"DELETE FROM voteUser WHERE userId='{userId}' AND boardId='{boardId}'"
		return super().deleteQuery(scode, sql)


	def getVoteUser(self, scode, userId, boardId):
		sql = f"SELECT * FROM voteUser WHERE userId='{userId}' AND boardId='{boardId}'"
		return super().selectOne(scode, sql)


	def getVoteUserList(self, scode, boardId):
		sql = f"SELECT * FROM voteUser WHERE boardId = '{boardId}'"
		return super().selectQuery(scode, sql)

	
	
	