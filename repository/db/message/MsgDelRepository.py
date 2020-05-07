from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository
from repository.db.message.MsgDelIdRepository import MsgDelIdRepository

class MsgDelRepository(MultiDbRepository):

	def insert(self, scode, channelId, userId, messageId):
		sql = f"INSERT INTO chatDelMessage (channelId, userId, messageId) VALUES('{channelId}', '{userId}', '{messageId}')"
		return super.insert(scode, sql)


	def getDelMessageIdList(self, scode, channelId, userId, joinAt):
		return MsgDelIdRepository().getList(channelId, userId, joinAt)


