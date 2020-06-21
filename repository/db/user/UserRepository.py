from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository
import time

class UserRepository(MultiDbRepository):

	def insert(self, scode, userId, userName, isAnonymous):
		return super().insert(scode, self.qInsert(userId, userName, isAnonymous)) 


	def insertDetail(self, scode, userId, userName, isAnonymous, osType, osVersion, appVersion):
		return super().insert(scode, self.qInsert(userId, userName, isAnonymous, osType, osVersion, appVersion)) 


	def updateUserDetail(self, scode, userId, osType, osVersion, appVersion):
		return super().update(scode, self.qUpdateUser(userId, osType, osVersion, appVersion))


	def delete(self, scode, userId):
		sql = f"DELETE FROM user WHERE userId='{userId}'"
		return super().delete(scode, sql)


	def getUser(self, scode, userId):
		sql = f"SELECT * FROM user WHERE userId='{userId}'"
		return super().selectOne(scode, sql)

	def getUserIdByUserName(self, scode, userName):
		sql = f"SELECT userId FROM user WHERE userName='{userName}'"
		return super().selectOne(scode, sql)

	def findUserName(self, scode, userName):
		sql = f"SELECT * FROM user WHERE userName='{userName}'"
		return super().selectOne(scode, sql) != None

	def updateAppCode(self, scode, userId, inAppcode):
		sql = f"UPDATE user SET inAppcode='{inAppcode}' WHERE userId='{userId}'"
		return super().update(scode, sql)


	def updateLastVisit(self, scode, userId):
		sql = f"UPDATE user SET lastAt=now() WHERE userId='{userId}'"
		return super().update(scode, sql)


	def updateLeave(self, scode, userId):
		sql = f"UPDATE user SET leftAt=now() WHERE userId='{userId}'"
		return super().update(scode, sql)


	def updateUsername(self, scode, userId, userName):
		sql = f"UPDATE user SET userName='{userName}', lastAt=now() WHERE userId='{userId}'"
		return super().update(scode, sql)


	def changeAnonymousToNormal(self, scode, userId):
		sql = f"UPDATE user SET anonymous=TRUE, lastAt=now() WHERE userId='{userId}'"
		return super().update(scode, sql)


	# def isSameAppCode(self, scode, inAppcode):
	# 	return this.inAppcode!=null && inAppcode.equals(inAppcode)


	def updateUserLike(self, scode, userId, likes, cancel):
		return super().update(scode, self.qUpdateUserLike(userId, likes, cancel))


	def qInsert(self, scode, userId, userName, isAnonymous):
		return f"INSERT INTO user (userId, userName, anonymous) VALUES('{userId}', '{userName}', {isAnonymous})"


	def qInsertDetail(self, scode, userId, userName, isAnonymous, osType, osVersion, appVersion):
		return f"INSERT INTO user (userId, userName, anonymous, osType, osVersion, appVersion, jointime, leavetime, lastAt) \
				 VALUES('{userId}', '{userName}', {isAnonymous}, '{osType}', '{osVersion}', '{appVersion}', {int(round(time.time() * 1000))}, 0, 0)"


	def qUpdateUser(self, userId, osType, osVersion, appVersion):
		return f"UPDATE user SET osType='{osType}', osVersion='{osVersion}', appVersion='{appVersion}', lastAt=now() WHERE userId='{userId}'"


	def qUpdateUserLike(self, scode, userId, likes, cancel):
		value = 1 if cancel == False else -1
		return f"UPDATE user SET likes=likes+{value} WHERE userId='{userId}'" if likes == True else f"UPDATE user SET dislikes=dislikes+{value} WHERE userId='{userId}'"
