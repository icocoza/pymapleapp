from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class MyChannelExtRepository(MultiDbRepository):


	def getChannelInfoList(self, scode, userId, offset, count):
		sql = f"SELECT chatMyChannel.channelId, chatChannel.userId, chatChannel.attendees, \
				chatMyChannel.modifiedAt, chatChannel.attendeeCount, channel.lastMessage \
				FROM chatMyChannel JOIN chatChannel ON(chatMyChannel.channelId = chatChannel.channelId) \
				WHERE chatMyChannel.userId='{userId}' ORDER BY chatMyChannel.modifiedAt DESC LIMIT {offset}, {count}"
		return self.selectQuery(scode, sql)

