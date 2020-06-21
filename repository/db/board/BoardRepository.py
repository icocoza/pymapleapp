from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class BoardRepository(MultiDbRepository):

	def insert(self, scode, boardId, userId, userName, title, shortContent, hasImage, hasFile, category, contentType):
		sql = f"INSERT INTO board (boardId, userId, userName, title, shortContent, hasImage, hasFile, category, contentType) \
				VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		params = (boardId, userId, userName, title, shortContent, hasImage, hasFile, category, contentType)
		return super().execute(scode, sql, params)
	
	def updateDelete(self, scode, boardId, userId):
		sql = f"UPDATE board SET deletedAt=NOW() WHERE userId='{userId}' AND boardId='{boardId}'"
		return super().updateQuery(scode, sql)

	def deleteBoard(self, scode, boardId, userId):
		sql = f"DELETE FROM board WHERE userId='{userId}' AND boardId='{boardId}'"
		return super().updateQuery(scode, sql)

	def updateBoard(self, scode, boardId, userId, title, shortContent, hasImage, hasFile, category, contentType):
		sql = f"UPDATE board SET title=%s, shortContent=%s, hasImage=%s, hasFile=%s, \
				category=%s, contentType=%s WHERE userId=%s AND boardId=%s"
		params = (title, shortContent, hasImage, hasFile, category, contentType, userId, boardId)
		return super().execute(scode, sql, params)
	
	def updateTitle(self, scode, boardId, userId, title):
		sql = f"UPDATE board SET title='{title}' WHERE userId='{userId}' AND boardId='{boardId}'"
		params = (title, userId, boardId)
		return super().execute(scode, sql, params)
	
	def updateContent(self, scode, boardId, userId, shortContent, hasImage, hasFile):
		sql = f"UPDATE board SET shortContent='{shortContent}', hasImage={hasImage}, hasFile={hasFile} WHERE userId='{userId}' AND boardId='{boardId}'"
		params = (shortContent, hasImage, hasFile, userId, boardId)
		return super().execute(scode, sql, params)	

	def updateCategory(self, scode, boardId, userId, category):
		sql = f"UPDATE board SET category='{category}' WHERE userId='{userId}' AND boardId='{boardId}'"
		params = (category, userId, boardId)
		return super().execute(scode, sql, params)

	def getListByCategory(self, scode, category, offset, count):
		sql = f"SELECT * FROM board WHERE category='{category}' ORDER BY createdAt DESC LIMIT {offset}, {count}"
		return super().selectQuery(scode, sql)
	
	def getListByUserId(self, scode, userId, category, offset, count):
		sql = f"SELECT * FROM board WHERE userId='{userId}' AND category='{category}' ORDER BY createdAt DESC LIMIT {offset}, {count}"
		return super().selectQuery(scode, sql)
	