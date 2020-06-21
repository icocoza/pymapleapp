from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class BoardContentRepository(MultiDbRepository):

	def insert(self, scode, boardId, userId, content):
		params = (boardId, userId, content)
		return super().execute(scode, self.qInsert(), params)

	def updateDelete(self, scode, boardId, userId):
		sql = "UPDATE boardContent SET deletedAt=NOW() WHERE userId=%s AND boardId=%s"
		params = (userId, boardId)
		return super().execute(scode, sql, params)

	def updateContent(self, scode, boardId, userId, content):
		sql = "UPDATE boardContent SET content=%s WHERE userId='%s AND boardId=%s"
		params = (content, userId, boardId)
		return super().updateQuery(scode, sql, params)

	def getContent(self, scode, boardId):
		sql = f"SELECT * FROM boardContent WHERE boardId='{boardId}'"
		return super().selectQuery(scode, sql)
    
	def qInsert(self):
		sql = 'INSERT INTO boardContent (boardId, userId, content) VALUES(%s, %s, %s)'
		return sql
