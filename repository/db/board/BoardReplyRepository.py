from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class BoardReplyRepository(MultiDbRepository):

	def insert(self, scode, replyId, boardId, parentId, userId, userName, depth, body):
		sql = f"INSERT INTO boardReply (replyId, parentId, boardId, userId, userName, depth, body) \
				VALUES('{replyId}', '{parentId}', '{boardId}', '{userId}', '{userName}', {depth}, '{body}')"
		return super().insertQuery(scode, sql)	

	def delete(self, scode, replyId, userId):
		sql = f"DELETE FROM boardReply WHERE replyId='{replyId}' AND userId='{userId}'"
		return super().deleteQuery(scode, sql)	

	def deleteIfNoChild(self, scode, replyId, boardId, userId):
		sql = f"SELECT replyId FROM boardReply WHERE parentId='{replyId}'"
		if(super().exist(scode, sql)==False):
			sql = f"DELETE FROM boardReply WHERE boardId='{boardId}' AND replyId='{replyId}' AND userId='{userId}'"
			return self.deleteQuery(scode, sql)		
		return super().updateMsg(replyId, userId, "-- deleted by user --")	

	def updateMsg(self, scode, replyId, userId, body):
		sql = f"UPDATE boardReply SET body='{body}' WHERE replyId='{replyId}' AND userId='{userId}'"
		return super().updateQuery(scode, sql)	

	def getList(self, scode, boardId, offset, count):
		sql = f"SELECT replyId, parentId, userId, userName, depth, body, replyAt FROM boardReply WHERE boardId='{boardId}' LIMIT {offset}, {count}"
		return super().selectQuery(scode, sql)
	