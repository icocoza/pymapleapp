from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class ChannelLastMsgRepository(MultiDbRepository):

	def getChannelLastMsg(self, scode, channelIds):
		channels = ','.join(["'" + str(id)+"'" for id in channelIds])
		sql = f"SELECT channelId, modifiedAt, lastMessage FROM chatChannel WHERE channelId IN({channels})"
		return super().selectQuery(scode, sql)