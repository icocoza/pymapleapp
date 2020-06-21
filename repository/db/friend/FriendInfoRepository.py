from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class FriendInfoRepository(MultiDbRepository):

	def getFriendMeList(self, scode, userId, friendType, offset, count):
		sql = f"SELECT userId, userName, userType, email FROM userAuth WHERE userId IN (SELECT userId FROM friend WHERE friendId='{userId}' LIMIT {offset}, {count})"
		if('all' != friendType):
			sql = f"SELECT userId, userName, userType, email FROM userAuth WHERE userId IN (SELECT userId FROM friend WHERE friendId='{userId}' AND friendType='{friendType}') LIMIT {offset}, {count}"
		return super().selectQuery(scode, sql)



