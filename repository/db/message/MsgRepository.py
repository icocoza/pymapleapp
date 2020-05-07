from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class MsgRepository(MultiDbRepository):


	def insert(self, scode, messageId, channelId, senderId, messageType, content):
		sql = f"INSERT INTO chatMessage (messageId, channelId, senderId, messageType, content) \
                VALUES('{messageId}', '{channelId}', '{senderId}', '{messageType}'', '{content}')"
		return super.insert(scode, sql)


	def delete(self, scode, messageId):
		sql = f"DELETE FROM chatMessage WHERE messageId='{messageId}'"
		return super.delete(scode, sql)


	def deleteChMsg(self, scode, channelId):
		sql = f"DELETE FROM chatMessage WHERE channelId='{channelId}'"
		return super.delete(scode, sql)


	def getMessage(self, scode, channelId, messageId):
		sql = f"SELECT * FROM chatMessage WHERE channelId='{channelId}' AND messageId='{messageId}'"
		return self.selectQuery(scode, sql)


	def getMessageList(self, scode, channelId, messageIds):
		ids = ','.join(["'" + str(id)+"'" for id in messageIds])
		sql = f"SELECT * FROM chatMessage WHERE channelId='{channelId}' AND messageId IN({ids})"
		return self.selectQuery(scode, sql)

    #SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
	def getMessageList(self, scode, channelId, joinAt, offset, count):
		strToDate = f"STR_TO_DATE('{datetime.strftime(joinAt, 'yyyy-MM-dd HH:mm:ss')}', '%Y-%m-%d %H:%i:%s')"
		sql = f"SELECT * FROM chatMessage WHERE channelId='{channelId}' AND createdAt > {strToDate} \
                ORDER BY createdAt DESC LIMIT {offset}, {count}"
		return self.selectQuery(scode, sql)


	def getMessageListWithoutDeletion(self, scode, channelId, joinAt, deleteIdsWithComma, offset, count):
		strToDate = f"STR_TO_DATE('{datetime.strftime(joinAt, 'yyyy-MM-dd HH:mm:ss')}', '%Y-%m-%d %H:%i:%s')"
		sql = f"SELECT * FROM chatMessage WHERE channelId='{channelId}' AND createdAt > {strToDate} AND messageId NOT IN({deleteIdsWithComma}) \
                ORDER BY createdAt DESC LIMIT {offset}, {count}"
		return self.selectQuery(scode, sql)


	def incReadCount(self, scode, messageId):
		sql = f"UPDATE chatMessage SET readCount = readCount+1 WHERE messageId='{messageId}'"
		return super.update(scode, sql)

