from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class ScrapDetailRepository(MultiDbRepository):

	def _selectToJson(self, scode, results):
		payload = []
		for item in results:
			scrapImg = f"http://{item[4]}:8080/scrap?scrapId={item[0]}"
			content = {'scrapId': item[0], 'url': item[1], 'title': item[2], 'subTitle': item[3], 'scrapIp': item[4], 'scrapPath': item[5], 'scrapExt': item[6], 'scrapimg': scrapImg, 'body': item[7]}
	
	def getScrapDetailList(self, scode, boardId):
		sql = f"SELECT * FROM scrap \
			    LEFT JOIN scrapbody ON scrap.scrapid = scrapbody.scrapid \
				LEFT JOIN boardscrap ON scrap.scrapid = boardscrap.scrapid \
				WHERE boardscrap.boardid='{boardId}'"
		return super().selectQuery(scode, sql)
