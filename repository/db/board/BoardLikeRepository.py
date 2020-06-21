from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class BoardLikeRepository(MultiDbRepository):


	def insert(self, scode, boardId, userId, userName, preferences):
		sql = f"INSERT INTO boardVoter (boardId, userId, userName, preferences) \
				VALUES('{boardId}', '{userId}', '{userName}', '{preferences}')"
		return super().insertQuery(scode, sql)

	def delete(self, scode, boardId):
		sql = f"DELETE FROM boardVoter WHERE boardId='{boardId}'"
		return super.delete(super().deleteQuery(scode, sql))

	def deletePreference(self, scode, boardId, userId, preferences ):
		sql = f"DELETE FROM boardVoter WHERE boardId='{boardId}' AND userId='{userId}' AND preferences='{preferences}'"
		return super.delete(super().deleteQuery(scode, sql))

	def getPreference(self, scode, boardId, userId):
		sql = f"SELECT userName, preferences FROM boardVoter WHERE boardId='{boardId}' AND userId='{userId}'"
		return super().selectQuery(scode, sql)