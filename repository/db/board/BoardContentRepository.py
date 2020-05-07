from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class BoardContentRepository(MultiDbRepository):

	def insert(self, scode, boardId, userId, content):
		sql = f"INSERT INTO boardContent (boardId, userId, content) VALUES('{boardId}', '{userId}', '{content}')"
		return self.insertQuery(scode, sql)

	def updateDelete(self, scode, boardId, userId):
		sql = f"UPDATE boardContent SET deletedAt=NOW() WHERE userId='{userId}' AND boardId='{boardId}'"
		return self.updateQuery(scode, sql)

	def updateContent(self, scode, boardId, userId, content):
		sql = f"UPDATE boardContent SET content='{content}' WHERE userId='{userId}' AND boardId='{boardId}'"
		return self.updateQuery(scode, sql)

	def getContent(self, scode, boardId):
		sql = f"SELECT * FROM boardContent WHERE boardId='{boardId}'"
		return self.selectQuery(scode, sql)
    
