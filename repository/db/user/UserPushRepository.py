from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class UserPushRepository(MultiDbRepository):


	def insert(self, scode, userId, uuid, epid):
		sql = f"INSERT INTO pushEpid (uuid, userId, epid) VALUES('{uuid}', '{userId}', '{epid}') \
				ON DUPLICATE KEY UPDATE userId='{userId}', epid='{epid}'"
		return self.insert(scode, sql)

	
	def delete(self, scode, uuid):
		sql = f"DELETE FROM pushEpid WHERE uuid='{uuid}'"
		return self.delete(scode, sql)


	def getEpid(self, scode, uuid):
		sql = f"SELECT * FROM pushEpid WHERE uuid='{uuid}'"
		return self.selectQuery(scode, sql)

	
	def updateEpid(self, scode, uuid, epid):
		sql = f"UPDATE pushEpid SET epid='{epid}' WHERE uuid='{uuid}'"
		return self.update(scode, sql)
