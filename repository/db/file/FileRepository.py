from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class FileRepository(MultiDbRepository):

	def insertFileInfo(self, scode, fileId, userId, fileName, fileType, fileSize, comment):
		sql = qInitFileInfo(fileId, userId, fileName, fileType, fileSize, comment)
		return super().insertQuery(scode, sql)


	def qInitFileInfo(self, scode, fileId, userId, fileName, fileType, fileSize, comment):
		return f"INSERT INTO uploadFile (fileId, userId, fileName, fileType, fileSize, comment) VALUES('{fileId}', '{userId}', \
				'{fileName}', '{fileType}', {fileSize}, '{comment}')"

	
	def updateFileInfo(self, scode, fileId, width, height, fileSize):
		sql = qUpdateFileInfo(fileId, width, height, fileSize)
		return super().insertQuery(scode, sql)


	def qUpdateFileInfo(self, scode, fileId, width, height, fileSize):
		return f"UPDATE uploadFile SET width={width}, height={height}, fileSize={fileSize}, uploaded=true WHERE fileId='{fileId}'"

	def updateCropped(self, scode, fileId, enabled):
		sql = f"UPDATE uploadFile SET cropped = {enabled} WHERE fileId='{fileId}'"
		return super().updateQuery(scode, sql)

	def updateFileEnabled(self, scode, fileId, boardId, enabled):
		sql = f"UPDATE uploadFile SET boardId='{boardId}', enabled={enabled}, deleted=false, deletedAt='' WHERE fileId='{fileId}' AND uploaded=true"
		return super().updateQuery(scode, sql)

	def updateFilesEnabled(self, scode, fileIds, boardId, enabled):
		files = ','.join(["'" + str(id)+"'" for id in fileIds])
		sql = f"UPDATE uploadFile SET boardId='{boardId}', enabled={enabled}, deleted=false, deletedAt=null WHERE fileId IN({files}) AND uploaded=true"
		return super().updateQuery(scode, sql)


	def updateThumbnail(self, scode, fileId, thumbWidth, thumbHeight):
		sql = qUpdateThumbnail(self, scode, fileId, thumbWidth, thumbHeight)
		return super().updateQuery(scode, sql)


	def qUpdateThumbnail(self, scode, fileId, thumbWidth, thumbHeight):
		return f"UPDATE uploadFile SET thumbWidth={thumbWidth}, thumbHeight={thumbHeight} WHERE fileId='{fileId}'",


	def updateDeleteFile(self, scode, boardId):
		sql = f"UPDATE uploadFile SET deleted=true, deletedAt=NOW() WHERE boardId='{boardId}'"
		return super().updateQuery(scode, sql)


	def delete(self, scode, fileId):
		sql = f"DELETE FROM uploadFile WHERE fileId='{fileId}'"
		return super().deleteQuery(scode, sql)


	def getFile(self, scode, fileId):
		sql = f"SELECT * FROM uploadFile WHERE fileId='{fileId}'"
		return super().selectQuery(scode, sql)

	
	def getFileList(self, scode, boardId):
		sql = f"SELECT fileId, fileName, fileType, fileSize, comment FROM uploadFile WHERE boardId='{boardId}' AND deletedAt is Null"
		return super().selectQuery(scode, sql)
