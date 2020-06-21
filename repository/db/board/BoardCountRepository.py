from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class BoardCountRepository(MultiDbRepository):

	def insert(self, scode, boardId):
		return super().insertQuery(scode, self.qInsert(scode, boardId))
	
	def incLike(self, scode, boardId, bInc):
		sql = f"UPDATE boardCount SET likes=likes+{1 if bInc else -1} WHERE  boardId='{boardId}'"
		return super().updateQuery(scode, sql)
	

	def incDislike(self, scode, boardId, bInc):
		sql = f"UPDATE boardCount SET dislikes=dislikes+{1 if bInc else -1} WHERE  boardId='{boardId}'"
		return super().updateQuery(scode, sql)
	

	def incVisit(self, scode, boardId):
		sql = f"UPDATE boardCount SET visit=visit+1 WHERE  boardId='{boardId}'"
		return super().updateQuery(scode, sql)
	

	def incReply(self, scode, boardId, bInc):
		sql = f"UPDATE boardCount SET reply=reply+{1 if bInc else -1} WHERE  boardId='{boardId}'"
		return super().updateQuery(scode, sql)

	def getCountInfo(self, scode, boardId):
		sql = f"SELECT * FROM boardCount WHERE  boardId='{boardId}'"
		return super().selectQuery(scode, sql)

	def qInsert(self, scode, boardId):
		return f"INSERT INTO boardCount(boardId) VALUES('{boardId}')"
