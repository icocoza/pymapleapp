from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class ChannelRepository(MultiDbRepository):

	def insert(self, scode, channelId, userId, attendees, attendeeCount, channelType):
		sql = f"INSERT INTO chatChannel (channelId, userId, attendees, attendeeCount, channelType) \
                VALUES('{channelId}', '{userId}', '{attendees}', {attendeeCount}, '{channelType}')"
		return self.insertQuery(scode, sql)


	def delete(self, scode, channelId):
		sql = f"DELETE FROM chatChannel WHERE channelId='{channelId}'"
		return self.deleteQuery(scode, sql)

	def updateAttendee(self, scode, channelId, attendees, attendeeCount, channelType):
		sql = f"UPDATE chatChannel SET attendees='{attendees}', attendeeCount={attendeeCount}, channelType='{channelType}' WHERE channelId='{channelId}'"
		return self.updateQuery(scode, sql)


	def updateLastTime(self, scode, channelId):
		sql = f"UPDATE chatChannel, chatMyChannel SET chatChannel.modifiedAt=now(), chatMyChannel.modifiedAt=now() \
                     WHERE chatChannel.channelId = chatMyChannel.channelId AND chatChannel.channelId='{channelId}'"
		return self.updateQuery(scode, sql)


	def updateLastMsgAndTime(self, scode, channelId, lastMessage):
		sql = f"UPDATE chatChannel, chatMyChannel SET chatChannel.modifiedAt = now(), chatMyChannel.modifiedAt = now(), \
                     chatChannel.lastMessage='{lastMessage}' WHERE chatChannel.channelId=chatMyChannel.channelId AND chatChannel.channelId='{channelId}'"
		return self.updateQuery(scode, sql)


	def getChannel(self, scode, channelId):
		sql = f"SELECT * FROM chatChannel WHERE channelId='{channelId}'"
		return self.selectQuery(scode, sql)


	def findChannel(self, scode, userId, attendees):
		sql = f"SELECT * FROM chatChannel WHERE (userId='{userId}' AND attendees='{attendees}') OR (userId='{attendees}' AND attendees='{userId}')"
		return self.selectQuery(scode, sql)


