from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository
from repository.db.channel.MyChannelExtRepository import MyChannelExtRepository

class MyChannelRepository(MultiDbRepository):

	def insert(self, scode, userId, channelId):
		sql = f"INSERT INTO chatMyChannel (userId, channelId) VALUES('{userId}', '{channelId}')"
		return super().insertQuery(scode, sql)


	def delete(self, scode, userId, channelId):
		sql = f"DELETE FROM chatMyChannel WHERE userId='{userId}' AND channelId='{channelId}'"
		return super().deleteQuery(scode, sql)


	def updateLastTime(self, scode, channelId):
		sql = f"UPDATE chatMyChannel SET modifiedAt=now() WHERE channelId='{channelId}'"
		return super().updateQuery(scode, sql)


	def getChannel(self, scode, userId, channelId):
		sql = f"SELECT * FROM chatMyChannel WHERE userId='{userId}' AND channelId='{channelId}'"
		return super().selectQuery(scode, sql)


	def getChannelList(self, scode, userId, offset, count):
		sql = f"SELECT * FROM chatMyChannel WHERE userId='{userId}' ORDER BY modifiedAt DESC LIMIT {offset}, {count}"
		return super().selectQuery(scode, sql)


	def getChannelCount(self, scode, userId):
		return super().count(f"SELECT COUNT(*) FROM chatMyChannel WHERE userId='{userId}'")

	def getChannelInfoList(self, scode, userId, offset, count):
		return MyChannelExtRepository().getChannelInfoList(userId, offset, count)


