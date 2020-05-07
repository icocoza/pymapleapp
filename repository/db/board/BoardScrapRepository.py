from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class BoardScrapRepository(MultiDbRepository):


	def insert(self, scode, boardId, scrapId):
		sql = qInsertScrap(boardId, scrapId)
		return self.insertQuery(scode, sql)
	
	def qInsertScrap(self, scode, boardId, scrapId):
		return f"INSERT INTO boardScrap (boardId, scrapId) VALUES('{boardId}', '{scrapId}')"
	
	def getScrapId(self, scode, boardId):
		sql = f"SELECT * FROM boardScrap WHERE boardId='{boardId}'"
		return self.selectQuery(scode, sql)
	
	def getScrapIdList(self, scode, boardId):
		sql = f"SELECT * FROM boardScrap WHERE boardId='{boardId}'"
		return self.selectQuery(scode, sql)
	
	def delete(self, scode, boardId):
		sql = f"DELETE FROM boardScrap WHERE boardId='{boardId}'"
		return self.deleteQuery(scode, sql)
	