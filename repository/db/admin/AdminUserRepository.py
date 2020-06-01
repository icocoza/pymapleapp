from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from repository.db.DbRepository import DbRepository

class AdminUserRepository(DbRepository):
    
    def insert(self, userId, email, password, userRole, userName):
        sql = f"INSERT INTO adminUser (userId, email, password, userRole, userName) \
                        VALUES('{userId}', '{email}', '{password}', '{userRole}', '{userName}')"
        return self.insertQuery(sql)
    
    def getUserByuserId(self, userId):
        sql = f"SELECT * FROM adminUser WHERE userId='{userId}'"
        return self.selectOne(sql)
    
    def getUserByEmail(self, email):
        sql = f"SELECT * FROM adminUser WHERE email='{email}'"
        return self.selectOne(sql)

    def getUserByUserIdPassword(self, userId, password):
        sql = f"SELECT * FROM adminUser WHERE userId='{userId}' AND password='{password}'"
        return self.selectOne(sql)

    def getUserList(self):
        sql = f"SELECT userId, email, userRole, userName FROM adminUser"
        return self.select(sql)

    def updateLastVisit(self, userId):
        sql = f"UPDATE adminUser SET lastAt=now() WHERE userId='{userId}'"
        return self.updateQuery(sql)

    def updateLeave(self, userId):
        sql = f"UPDATE adminUser SET password='', leftAt=now(), lastAt=now() WHERE userId='{userId}'"
        return self.updateQuery(sql)

    def updatePassword(self, userId, oldPass, newPass):
        sql = f"UPDATE adminUser SET password='{newPass}', lastPassword='{oldPass}', passwordAt=now(), lastAt=now() \
                WHERE userId='{userId}' AND password='{oldPass}"
        return self.updateQuery(sql)

