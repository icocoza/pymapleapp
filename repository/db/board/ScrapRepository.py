from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class ScrapRepository(MultiDbRepository):

	def insert(self, scode, scrapId, url, title, subTitle):
		sql = qInsertScrap(scrapId, url, title, subTitle)
		return super().insertQuery(scode, sql)

	def qInsertScrap(self, scode, scrapId, url, title, subTitle):
		return f"INSERT INTO scrap (scrapId, url, title, subTitle) VALUES('{scrapId}', '{url}', '{title}', '{subTitle}')"
	
	def getScrap(self, scode, scrapId):
		sql = f"SELECT * FROM scrap WHERE scrapId='{scrapId}'"
		return super().selectQuery(scode, sql)

	def getScrapList(self, scode, scrapIds):
		ids = ','.join(["'" + str(id)+"'" for id in scrapIds])
		sql = f"SELECT * FROM scrap WHERE scrapId IN ({ids})"
		return super().selectQuery(scode, sql)

	def getScrapListByUrl(self, scode, url):
		sql = f"SELECT * FROM scrap WHERE url = '{url}'"
		return super().selectQuery(scode, sql)
	
	def updateScrapFile(self, scode, scrapId, fileName):
		sql = f"UPDATE scrap SET fileName='{fileName}' WHERE scrapId='{scrapId}'"
		return super().updateQuery(scode, sql)

