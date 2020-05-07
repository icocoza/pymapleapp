from inspect import getsourcefile
import os.path as path, sys
from datetime import datetime
import hashlib
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.MultiDbRepository import MultiDbRepository

class UserAuthRepository(MultiDbRepository):

	def insertUserIdPw(self, scode, userId, userName, password):
		return self.insert(qInsertUserNamePw(userId, password))


	def qInsertUserNamePw(self, scode, userId, userName, password):
		password = hashlib.sha256(password.encode()).hexdigest()
		return f"INSERT INTO userAuth (userId, password, authType) VALUES('{userId}', '{password}', 'idpw')"


	def insertEmail(self, scode, userId, email):
		return self.insert(qInsertEmail(userId, email))


	def qInsertEmail(self, scode, userId, email):
		return f"INSERT INTO userAuth (userId, email, authType) VALUES('{userId}', '{email}', 'email')"


	def insertPhoneNo(self, scode, userId, mobileNo):
		return self.insert(qInsertPhoneNo(userId, mobileNo))


	def qInsertPhoneNo(self, scode, userId, mobileNo):
		return f"INSERT INTO userAuth (userId, mobileNo, authType) VALUES('{userId}', '{mobileNo}', 'mobile')"

	def getUser(self, scode, userId):
		sql = f"SELECT * FROM userAuth WHERE userId='{userId}'"
		return self.selectQuery(scode, sql)

	def getUserByUserName(self, scode, userName):
		sql = f"SELECT * FROM userAuth WHERE userName='{userName}'"
		return self.selectQuery(scode, sql)

	def findUserId(self, scode, userId):
		return self.getUser(scode, userId) != None

	def findUserName(self, scode, userName):
		return self.getUserByUserName(scode, userName) != None

	def getUserByEmail(self, scode, email):
		sql = f"SELECT * FROM userAuth WHERE email='{email}'"
		return self.selectQuery(scode, sql)

	def findEmail(self, scode, email):
		return self.getUserByEmail(scode, email) != None

	
	def getUserByMobile(self, scode, mobileNo):
		sql = f"SELECT * FROM userAuth WHERE mobileNo='{mobileNo}'"
		return self.selectQuery(scode, sql)

	def findMobile(self, scode, mobileNo):
		return self.getUserByMobile(scode, mobileNo) != None

	def findUserAuth(self, scode, userId, email, mobileNo):
		sql = f"SELECT * FROM userAuth WHERE userId='{userId}' OR email='{email}' OR mobileNo='{mobileNo}'"
		auth = self._selectToJson(self.selectQuery(scode, sql))
		if len(auth) < 1:
			return None
		return auth['authType']

	def updatePw(self, scode, userId, password):
		return self.update(qUpdatePw(userId, password))


	def qUpdatePw(self, scode, userId, password):
		password = hashlib.sha256(password.encode()).hexdigest()
		return f"UPDATE userAuth SET password='{password}' WHERE userId='{userId}'"

	def updateEmailCode(self, scode, email, emailCode):
		return self.update(qUpdateEmailCode(email, emailCode))


	def qUpdateEmailCode(self, scode, email, emailCode):
		return f"UPDATE userAuth SET emailCode='{emailCode}' WHERE email='{email}'"

	def updateSMSCode(self, scode, mobileNo, smsCode):
		return self.update(qUpdateSMSCode(mobileNo, smsCode))


	def qUpdateSMSCode(self, scode, mobileNo, smsCode):
		return f"UPDATE userAuth SET smsCode='{smsCode}' WHERE mobileNo='{mobileNo}'"


	def updateUserQuit(self, scode, userId):
		sql = f"UPDATE userAuth SET authType='quit' WHERE userId='{userId}'"
		return self.update(scode, sql)


	def deleteUser(self, scode, userId):
		sql = f"DELETE FROM userAuth WHERE userId='{userId}'"
		return self.delete(scode, sql)


	# def isSameAuthId(self, scode, authType, userId ):
	# 	if('idpw' == authType and this.userId.equals(userId))
	# 		return true
    #     if(EUserAuthType.email == authType && this.email != null && this.email.equals(userId))
    #         return true
    #     if(EUserAuthType.mobileNo == authType && this.mobileNo != null && this.mobileNo.equals(userId))
    #         return true
    #     return false


    # def isSameUserName(self, scode, userId):
    #     return this.userId!=null && this.userId.equals(userId)


    # def isSamePw(self, scode, password):
    #     password = StrUtils.getSha256(password)
    #     return this.password != null && this.password.equals(password)


    # def isSameSmsCode(self, scode, smsCode):
    #     return this.smsCode!=null && this.smsCode.equals(smsCode)
