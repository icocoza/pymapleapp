from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class ScrapRepository(MultiDbRepository):

	def insert(self, scode, scrapId, url, title, subTitle):
		sql = qInsertScrap(scrapId, url, title, subTitle)
		return self.insertQuery(scode, sql)

	def qInsertScrap(self, scode, scrapId, url, title, subTitle):
		return f"INSERT INTO scrap (scrapId, url, title, subTitle) VALUES('{scrapId}', '{url}', '{title}', '{subTitle}')"
	
	def getScrap(self, scode, scrapId):
		sql = f"SELECT * FROM scrap WHERE scrapId='{scrapId}'"
		return self.selectQuery(scode, sql)

	def getScrapList(self, scode, scrapIds):
		ids = ','.join(["'" + str(id)+"'" for id in scrapIds])
		sql = f"SELECT * FROM scrap WHERE scrapId IN ({ids})"
		return self.selectQuery(scode, sql)

	def getScrapListByUrl(self, scode, urls):
		urllist = ','.join(["'" + str(id)+"'" for id in urls])
		sql = f"SELECT * FROM scrap WHERE url IN ({urllist})"
		return self.selectQuery(scode, sql)
	
	def updateScrapFile(self, scode, scrapId, fileName):
		sql = f"UPDATE scrap SET fileName='{fileName}' WHERE scrapId='{scrapId}'"
		return self.updateQuery(scode, sql)

