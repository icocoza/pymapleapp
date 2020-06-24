from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class BoardDetailRepository(MultiDbRepository):

	def getBoardList(self, scode, category, offset,  count):
		sql = f"SELECT board.boardId, board.userId, board.userName, board.title, board.shortContent, board.hasImage, board.hasFile, board.category, \
	   			board.contentType, board.createdAt, boardCount.likes, boardCount.dislikes, boardCount.visit, boardCount.reply FROM board \
				LEFT JOIN boardCount ON board.boardId=boardCount.boardId \
				LEFT JOIN boardScrap ON board.boardId=boardScrap.boardId \
				LEFT JOIN scrap ON scrap.scrapId=boardScrap.scrapId \
				WHERE board.category='{category}' AND board.deletedAt is NULL ORDER BY board.createdAt DESC LIMIT {offset}, {count}"
		return super().selectQuery(scode, sql)
	
	def getBoardListByIds(self, scode, boardIds):
		ids = ','.join(["'" + str(id)+"'" for id in boardIds])
		sql = f"SELECT board.boardId, board.userId, board.userName, board.title, board.shortContent, board.hasImage, board.hasFile, board.category, \
	   			board.contentType, board.createdAt, boardCount.likes, boardCount.dislikes, boardCount.visit, boardCount.reply FROM board FROM board \
				LEFT JOIN boardCount ON board.boardId=boardCount.boardId \
				LEFT JOIN boardScrap ON board.boardId=boardScrap.boardId \
				LEFT JOIN scrap ON scrap.scrapId=boardScrap.scrapId \
				WHERE board.boardId IN ({ids}) ORDER BY FIELD(board.boardId, {ids})"
		return super().selectQuery(scode, sql)
	
	def getCropfilePath(self, scode, rec):
		if(rec.fileName==None or len(rec.fileName) < 1):
			return None
		return f"http://{rec.serverIp}:8080/{rec.subPath}?boardId={rec.boardId}&scode={scode}"

