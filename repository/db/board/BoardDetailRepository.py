from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class BoardDetailRepository(MultiDbRepository):

	def getBoardList(self, scode, category, offset,  count):
		sql = f"SELECT * FROM board \
				LEFT JOIN boardcount ON board.boardid=boardcount.boardid \
				LEFT JOIN filecrop ON board.boardid=filecrop.boardid \
				LEFT JOIN boardscrap ON board.boardid=boardscrap.boardid \
				LEFT JOIN scrap ON scrap.scrapid=boardscrap.scrapid \
				WHERE board.category='{category}' AND board.deleted=false ORDER BY board.createtime DESC LIMIT {offset}, {count}"
		return super().selectQuery(scode, sql)
	
	def getBoardListByIds(self, scode, boardIds):
		ids = ','.join(["'" + str(id)+"'" for id in boardIds])
		sql = f"SELECT * FROM board \
				LEFT JOIN boardcount ON board.boardid=boardcount.boardid \
				LEFT JOIN filecrop ON board.boardid=filecrop.boardid \
				LEFT JOIN boardscrap ON board.boardid=boardscrap.boardid \
				LEFT JOIN scrap ON scrap.scrapid=boardscrap.scrapid \
				WHERE board.boardid IN ({ids}) ORDER BY FIELD(board.boardid, {ids})"
		return super().selectQuery(scode, sql)
	
	def getCropfilePath(self, scode, rec):
		if(rec.fileName==None or len(rec.fileName) < 1):
			return None
		return f"http://{rec.serverIp}:8080/{rec.subPath}?boardid={rec.boardId}&scode={scode}"

