from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class ScrapBodyRepository(MultiDbRepository):

	
	def insert(self, scode, scrapId,  body):
		sql = qInsertScrapBody(scrapId, body)
		return self.insertQuery(scode, sql)


	def qInsertScrapBody(self, scode, scrapId, body):
		return f"INSERT INTO scrapBody (scrapId, body) VALUES('{scrapId}', '{body}')"

	
	def getScrapBody(self, scode, scrapId):
		sql = f"SELECT * FROM scrapBody WHERE scrapId='{scrapId}'"
		return self.selectQuery(scode, sql)

		
	def updateScrapBody(self, scode, scrapId, body):
		sql = f"UPDATE scrapBody SET body='{body}' WHERE scrapId='{scrapId}'"
		return self.updateQuery(scode, sql)