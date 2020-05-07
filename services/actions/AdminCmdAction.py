import os, sys, json, datetime
from services.constant.MapleCmd import MapleCmd
from common.utils.StrUtils import StrUtils
from services.constant.AllError import AllError
from services.actions.Action import Action
from services.actions.admin.AdminToken import AdminToken

from repository.db.admin.AdminUserRepository import AdminUserRepository
from repository.db.admin.AdminTokenRepository import AdminTokenRepository
from repository.db.admin.AdminAppRepository import AdminAppRepository

from module.db.MultiDbHelper import MultiDbHelper
import common.utils.keygen as keygen

class AdminCmdAction(Action):
    def __init__(self):
        super().__init__()

        self.adminToken = AdminToken()
        self.adminUserRepository = AdminUserRepository ()
        self.adminTokenRepository = AdminTokenRepository()
        self.adminAppRepository = AdminAppRepository()
        self.mapleCmd = MapleCmd()

        self.funcMap = {}
        self.funcMap[self.mapleCmd.EAdminCmd().adminRegister.name] = lambda jdata: adminRegister(jdata)
        self.funcMap[self.mapleCmd.EAdminCmd().adminLogin.name] = lambda jdata: adminLogin(jdata)
        self.funcMap[self.mapleCmd.EAdminCmd().adminLogout.name] = lambda jdata: adminLogout(jdata)
        self.funcMap[self.mapleCmd.EAdminCmd().adminAddApp.name] = lambda jdata: addApp(jdata)
        self.funcMap[self.mapleCmd.EAdminCmd().adminDelApp.name] = lambda jdata: delApp(jdata)
        self.funcMap[self.mapleCmd.EAdminCmd().adminAppList.name] = lambda jdata: appList(jdata)
        self.funcMap[self.mapleCmd.EAdminCmd().adminModifyApp.name] = lambda jdata: modifyApp(jdata)
        self.funcMap[self.mapleCmd.EAdminCmd().adminAppCount.name] = lambda jdata: appCount(jdata)
        
        self.funcMap[self.mapleCmd.EAdminCmd().adminStopApp.name] = lambda jdata: updateAppStatus(jdata)
        self.funcMap[self.mapleCmd.EAdminCmd().adminReadyApp.name] = lambda jdata: updateAppStatus(jdata)
        self.funcMap[self.mapleCmd.EAdminCmd().adminRunApp.name] = lambda jdata: updateAppStatus(jdata)

    def adminRegister(self, jdata):
        if StrUtils.isEmail(jdata['email']) == False:
            return self.setError('admin', AllError.InvalidEmailFormat)
        if self.adminUserRepository.getUserByEmail(jdata['email']) == None:
            return self.setError('admin', AllError.ExistEmail)
        if len(jdata['password']) < 8:
            return self.setError('admin', AllError.ShortPasswordLengthThan8)

        userId = StrUtils.getSha256Uuid('adminId:')
        if self.adminUserRepository.insert(userId, jdata['email'], StrUtils.getSha256(jdata['password']), 'user', jdata['userName']) == False:
            return self.setError('admin', AllError.RegisterFailed)
        return self.setOk('admin', userId)

    def adminLogin(self, jdata):
        user = self.adminUserRepository.getUserByEmail(jdata['email'])
        if user == None:
            return self.setError('admin', AllError.NotExistUser)
        if StrUtils.getSha256(jdata['password']) != user['password']:
            return self.setError('admin', AllError.WrongAccountInfo)
        
        token = self.adminToken.createUser(user['userId'], user['userRole'], user['userName'])
        self.adminTokenRepository.upsert(user['userId'], token, '0.0.0.0')
        return self.setOk('admin', {'userId': user['userId'], 'token': token})

    def adminLogout(self, jdata):
        if 'token' not in jdata:
            return self.setError('admin', AllError.InvalidAdminToken)
        token = self.adminToken.parseUser(jdata['token'])
        if token == None:
            return self.setError('admin', AllError.InvalidAdminToken)
        if self.adminToken.isExpired(token['expireAt']) == True:
            return self.setError('admin', AllError.ExpiredAdminToken)
        if self.adminTokenRepository.isAvailableToken(jdata['userId'], jdata['token']) == False:
            return self.setError('admin', AllError.UnauthorizedOrExpiredUser)
        
        return self.setOk('admin', token['userId'])

    def addApp(self, jdata):
        ret = self.__checkAdminToken(jdata)
        if ret is Action:
            return ret
        token = ret
        scode = jdata['scode']
        if StrUtils.isAlphaNumeric(scode) == False:
            return self.setError('admin', AllError.ScodeAllowedOnlyAlphabet)
        if self.adminAppRepository.hasAdminSCode(scode) == True:
            return self.setError('admin', AllError.AlreadyExistScode)

        appId = keygen.createKey('appId')
        appToken = self.adminToken.createApp(appId, scode)

        ret = self.__createAppDatabase(scode, jdata)
        if ret != None:
            return ret
        MultiDbHelper.createTables(scode)
        #appId, userId, scode, token, title, description, status
        if self.adminAppRepository.insertApp(appId, token['userId'], scode, appToken, jdata['title'], jdata['description'], jdata['appstatus']) == False:
            return self.setError('admin', AllError.failedToCreateApp)
        if 'fcmId' in jdata and 'fcmKey' in jdata:
            self.adminAppRepository.updateAdminPush(token['userId'], scode, jdata['fcmId'], jdata['fcmKey'])
        return self.setOk('admin', {'appId': appId, 'appToken': appToken})

    def delApp(self, jdata):
        ret = self.__checkAdminToken('admin', jdata, passwd=True)
        if ret is Action:
            return ret
        token = ret
        scode = jdata['scode']
        if self.adminAppRepository.getAppByScode(token['userId'], scode) is None:
            return self.setError('admin', AllError.NotExistScode)

        self.adminAppRepository.updateAdminAppStatus(token['userId'], scode, 'deleted')
        return self.setOk('admin', token['userId'])

    def appList(self, jdata):
        ret = self.__checkAdminToken('admin', jdata)
        if ret is Action:
            return ret
        token = ret
        appList = self.adminAppRepository.getAppList(token['userId'])
        if len(appList) < 1:
            return self.setError('admin', AllError.NoListData)

        return self.setOk('admin', {'appList': appList})

    def modifyApp(self, jdata):
        ret = self.__checkAdminToken('admin', jdata, passwd=True)
        if ret is Action:
            return ret
        token = ret
        scode = jdata['scode']

        if self.adminAppRepository.updateApp(token['userId'], scode, jdata['title'], jdata['description'], jdata['status']) == False:
            return self.setError('admin', AllError.FailedToUpdateApp)
        if 'fcmId' in jdata and 'fcmKey' in jdata:
            self.adminAppRepository.updatePushInfo(token['userId'], scode, jdata['fcmId'], jdata['fcmKey'])
        return self.setOk('admin', jdata)

    def appCount(self, jdata):
        ret = self.__checkAdminToken('admin', jdata)
        if ret is Action:
            return ret
        token = ret
        count = self.adminAppRepository.getAppCount(token['userId'], jdata['status'])
        return self.setOk('admin', {'count': count})

    def updateAppStatus(self, jdata):
        ret = self.__checkAdminToken('admin', jdata, passwd=True)
        if ret is Action:
            return ret
        token = ret
        scode = jdata['scode']
        if self.adminAppRepository.updateStatus(token['userId'], scode, jdata['status']) == False:
            return self.setError('admin', AllError.FailedToUpdateApp)
        return self.setOk('admin', scode)

    def __checkAdminToken(self, jdata, passwd=False):
        if 'token' not in jdata:
            return self.setError('admin', AllError.InvalidAdminToken)
        token = self.adminToken.parseUser(jdata['token'])
        if token == None:
            return self.setError('admin', AllError.InvalidAdminToken)
        if self.adminToken.isExpired(token['expireAt']) == True:
            return self.setError('admin', AllError.ExpiredAdminToken)
        if self.adminTokenRepository.isAvailableToken(token['userId'], jdata['token']) == False:
            return self.setError('admin', AllError.UnauthorizedOrExpiredUser)
        if passwd:
            user = AdminUserRepository.getUserByUserIdPassword(token['userId'], jdata['password'])
            if user is None:
                return self.setError('admin', AllError.UnauthorizedUser)
        return token

    def __createAppDatabase(self, jdata):
        scode = jdata['scode']
        if 'host' not in jdata or 'userId' not in jdata or 'password' not in jdata:
            if MultiDbHelper.instance().createDatabaseWithDefault(scode) == False:
                return self.setError('admin', AllError.FailedToCreateDatabase)
            MultiDbHelper.instance().initMysqlWithDefault(scode)
        else:
            if MultiDbHelper.instance().createDatabase(scode, jdata['host'], jdata['port'], jdata['userId'], jdata['password']) == False:
                return self.setError('admin', AllError.FailedToCreateDatabase)
            MultiDbHelper.instance().initMySql(scode, jdata['host'], jdata['port'], jdata['userId'], jdata['password'], scode)
