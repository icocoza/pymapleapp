from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class MsgDelIdRepository(MultiDbRepository):

       #SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
	def getList(self, scode, channelId, userId, joinAt):
		strToDate = f"STR_TO_DATE('{joinAt.strftime('yyyy-MM-dd hh:mm:ss')}', '%Y-%m-%d %H:%i:%s')"
		sql = f"SELECT messageId FROM chatDelMessage WHERE channelId='{channelId}' AND userId='{userId}' AND createdAt > {strToDate}"
		return self.selectQuery(scode, sql)

