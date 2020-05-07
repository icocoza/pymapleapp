from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class BoardVoteUserCountRepository(MultiDbRepository):

	def getVoteCount(self, scode, boardIds):
		ids = ','.join(["'" + str(id)+"'" for id in boardIds])
		sql = f"SELECT boardId, count(boardId) as voteCount FROM voteUser WHERE boardId in ({ids}) group by boardId"
		return self.selectQuery(scode, sql)

	def getVotedBoardId(self, scode, userId, boardIds):
		ids = ','.join(["'" + str(id)+"'" for id in boardIds])
		sql = f"SELECT boardId FROM voteUser WHERE boardId in ({ids}) AND userId='{userId}'"
		return self.selectQuery(scode, sql)
	
	
	