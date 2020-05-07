from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class BoardVoteItemRepository(MultiDbRepository):

	def insert(self, scode, boardId, voteItemId, itemText):
		sql = f"INSERT INTO voteItem (voteItemId, boardId, itemText) VALUES('{voteItemId}','{boardId}','{itemText}')"
		return self.insertQuery(scode, sql)
	

	def incVoteItem(self, scode, boardId, voteItemId):
		sql = f"UPDATE voteItem SET selectcount=selectcount+1 WHERE voteItemId='{voteItemId}' AND boardId='{boardId}'"
		return self.updateQuery(scode, sql)
	

	def decVoteItem(self, scode, boardId, voteItemId):
		sql = f"UPDATE voteItem SET selectcount=selectcount-1 WHERE voteItemId='{voteItemId}' AND boardId='{boardId}'"
		return self.updateQuery(scode, sql)
	

	def updateVoteText(self, scode, boardId, voteItemId, itemText):
		sql = f"UPDATE voteItem SET itemText='{itemText}' WHERE boardId ='{boardId}' AND voteItemId='{voteItemId}'"
		return self.updateQuery(scode, sql)
	

	def deleteVote(self, scode, boardId):
		sql = f"DELETE FROM voteItem WHERE boardId='{boardId}'"
		return self.deleteQuery(scode, sql)
	
	def deleteVoteItem(self, scode, boardId, voteItemId):
		sql = f"DELETE FROM voteItem WHERE boardId='{boardId}' AND voteItemId='{voteItemId}'"
		return self.deleteQuery(scode, sql)
	

	def getVoteItemList(self, scode, boardId):
		sql = f"SELECT * FROM voteItem WHERE boardId='{boardId}'"
		return self.selectQuery(scode, sql)
	
	