from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository
from repository.db.friend.FriendInfoRepository import FriendInfoRepository

class FriendRepository(MultiDbRepository):

	
	def insert(self, scode, userId, friendId, friendName, friendType):
		params = (userId, friendId, friendName, friendType)
		sql = f"INSERT INTO friend (userId, friendId, friendName, friendType) VALUES(%s, %s, %s, %s)"
		return super().execute(scode, sql, params)

	def delete(self, scode, userId, friendId):
		sql = f"DELETE FROM friend WHERE userId='{userId}' AND friendId='{friendId}'"
		return super().delete(scode, sql)

	def updateFriendType(self, scode, userId, friendId, friendType):
		sql = f"UPDATE friend SET friendType='{friendType}' WHERE userId='{userId}' AND friendId='{friendId}'"
		return super().update(scode, sql)

	def getListByType(self, scode, userId, friendType, offset, count):
		if('all' == friendType):
			return self.getListAll(scode, userId, offset, count)
		sql = f"SELECT * FROM friend WHERE userId='{userId}' AND friendType='{friendType}' LIMIT {offset}, {count}"
		return super().selectQuery(scode, sql)

	def getListAll(self, scode, userId, offset, count):
		sql = f"SELECT * FROM friend WHERE userId='{userId}' LIMIT {offset}, {count}"
		return super().selectQuery(scode, sql)

	def getListByIds(self, scode, userId, friendIds):
		friends = ','.join(["'" + str(id)+"'" for id in friendIds])
		sql = f"SELECT * FROM friend WHERE userId='{userId}' AND friendId IN ({friends})"
		return super().selectQuery(scode, sql)

	def getCount(self, scode, userId, friendType):
		if('all' == friendType):
			return super().count(scode, f"SELECT friendId FROM friend WHERE userId='{userId}'")
		return super().count(scode, f"SELECT friendId FROM friend WHERE userId='{userId}' AND friendType='{friendType}'")

	def getFriendMeCount(self, scode, userId, friendType):
		if('all' == friendType):
			return super().count(scode, f"SELECT friendId FROM friend WHERE friendId='{userId}'")
		return super().count(scode, f"SELECT friendId FROM friend WHERE friendId='{userId}' AND friendType='{friendType}'")

	def getFriendMeList(self, scode, userId, friendType, offset, count):
		return FriendInfoRepository().getFriendMeList(userId, friendType, offset, count)



