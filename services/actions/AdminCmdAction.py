import os, sys, json, datetime
from services.constant.MapleCmd import EAdminCmd
import common.utils.StrUtils as StrUtils
from services.constant.AllError import AllError
from services.actions.Action import Action
from services.actions.admin.AdminToken import AdminToken

from repository.db.admin.AdminUserRepository import AdminUserRepository
from repository.db.admin.AdminTokenRepository import AdminTokenRepository
from repository.db.admin.AdminAppRepository import AdminAppRepository

from module.db.MultiDbHelper import MultiDbHelper
import common.utils.keygen as keygen

import logging

class AdminCmdAction(Action):
    def __init__(self):
        super().__init__()

        self.adminToken = AdminToken()
        self.adminUserRepository = AdminUserRepository ()
        self.adminTokenRepository = AdminTokenRepository()
        self.adminAppRepository = AdminAppRepository()

        self.funcMap = {}
        self.funcMap[EAdminCmd.adminAdminRegister.name] = lambda jdata: self.adminAdminRegister(jdata)
        self.funcMap[EAdminCmd.adminRegister.name] = lambda jdata: self.adminRegister(jdata)
        self.funcMap[EAdminCmd.adminLogin.name] = lambda jdata: self.adminLogin(jdata)
        self.funcMap[EAdminCmd.adminLogout.name] = lambda jdata: self.adminLogout(jdata)
        self.funcMap[EAdminCmd.adminAddApp.name] = lambda jdata: self.addApp(jdata)
        self.funcMap[EAdminCmd.adminDelApp.name] = lambda jdata: self.delApp(jdata)
        self.funcMap[EAdminCmd.adminAppList.name] = lambda jdata: self.appList(jdata)
        self.funcMap[EAdminCmd.adminModifyApp.name] = lambda jdata: self.modifyApp(jdata)
        self.funcMap[EAdminCmd.adminAppCount.name] = lambda jdata: self.appCount(jdata)
        
        self.funcMap[EAdminCmd.adminStopApp.name] = lambda jdata: self.updateAppStatus(jdata)
        self.funcMap[EAdminCmd.adminReadyApp.name] = lambda jdata: self.updateAppStatus(jdata)
        self.funcMap[EAdminCmd.adminRunApp.name] = lambda jdata: self.updateAppStatus(jdata)

        self.funcMap[EAdminCmd.adminUserList.name] = lambda jdata: self.adminUserList(jdata)

    def adminAdminRegister(self, jdata):
        jdata['role'] = 'admin'
        return self.__userRegister(jdata)
    
    def adminRegister(self, jdata):
        jdata['role'] = 'user'
        return self.__userRegister(jdata)

    def __userRegister(self, jdata):
        if StrUtils.isEmail(jdata['email']) == False:
            return self.setError('admin', AllError.InvalidEmailFormat)
        if self.adminUserRepository.getUserByEmail(jdata['email']) is not None:
            return self.setError('admin', AllError.ExistEmail)
        if len(jdata['password']) < 8:
            return self.setError('admin', AllError.ShortPasswordLengthThan8)

        userId = StrUtils.getMapleUuid('adminId:')
        if self.adminUserRepository.insert(userId, jdata['email'], StrUtils.getSha256(jdata['password']), jdata['role'], jdata['userName']) == False:
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
        if isinstance(ret, dict) and 'result' in ret:
            return ret
        token = ret
        scode = jdata['scode']
        if StrUtils.isAlphaNumeric(scode) == False:
            return self.setError('admin', AllError.ScodeAllowedOnlyAlphabet.name())
        if self.adminAppRepository.hasSCode(scode) == True:
            return self.setError('admin', AllError.AlreadyExistScode)

        appId = keygen.createKey('appId:')
        appToken = self.adminToken.createApp(appId, scode)

        ret = self.__createAppDatabase(scode, jdata)
        if ret != None:
            return ret
        MultiDbHelper.instance().createTables(scode)
        #appId, userId, scode, token, title, description, status
        if self.adminAppRepository.insertApp(appId, token['userId'], scode, appToken, jdata['title'], jdata['description'], jdata['status']) == False:
            return self.setError('admin', AllError.failedToCreateApp)
        if 'dbHost' in jdata and 'dbPort' in jdata and 'dbUser' in jdata and 'dbPassword'in jdata:
            self.adminAppRepository.updateExternalDbInfo(token['userId'], scode, jdata['dbHost'], jdata['dbPort'], jdata['dbUser'], jdata['dbPassword'])
        if 'fcmId' in jdata and 'fcmKey' in jdata:
            self.adminAppRepository.updateAdminPush(token['userId'], scode, jdata['fcmId'], jdata['fcmKey'])
        return self.setOk('admin', {'appId': appId, 'appToken': appToken})

    def delApp(self, jdata):
        ret = self.__checkAdminToken('admin', jdata, passwd=True)
        if isinstance(ret, dict) and 'result' in ret:
            return ret
        token = ret
        scode = jdata['scode']
        if self.adminAppRepository.getAppByScode(token['userId'], scode) is None:
            return self.setError('admin', AllError.NotExistScode)

        self.adminAppRepository.updateAdminAppStatus(token['userId'], scode, 'deleted')
        return self.setOk('admin', token['userId'])

    def appList(self, jdata):
        ret = self.__checkAdminToken(jdata)
        if isinstance(ret, dict) and 'result' in ret:
            return ret
        token = ret
        appList = self.adminAppRepository.getAppList(token['userId'])
        if appList is None:
            return self.setError('admin', AllError.NoListData)

        return self.setOk('admin', {'appList': appList})

    def modifyApp(self, jdata):
        ret = self.__checkAdminToken(jdata, passwd=True)
        if isinstance(ret, dict) and 'result' in ret:
            return ret
        token = ret
        scode = jdata['scode']

        if self.adminAppRepository.updateApp(token['userId'], scode, jdata['title'], jdata['description'], jdata['status']) == False:
            return self.setError('admin', AllError.FailedToUpdateApp)
        if 'fcmId' in jdata and 'fcmKey' in jdata:
            self.adminAppRepository.updatePushInfo(token['userId'], scode, jdata['fcmId'], jdata['fcmKey'])
        return self.setOk('admin', jdata)

    def appCount(self, jdata):
        ret = self.__checkAdminToken(jdata)
        if isinstance(ret, dict) and 'result' in ret:
            return ret
        token = ret
        count = self.adminAppRepository.getAppCount(token['userId'], jdata['status'])
        return self.setOk('admin', {'count': count})

    def updateAppStatus(self, jdata):
        ret = self.__checkAdminToken(jdata, passwd=True)
        if isinstance(ret, dict) and 'result' in ret:
            return ret
        token = ret
        scode = jdata['scode']
        if self.adminAppRepository.updateStatus(token['userId'], scode, jdata['status']) == False:
            return self.setError('admin', AllError.FailedToUpdateApp)
        return self.setOk('admin', scode)

    def adminUserList(self, jdata):
        ret = self.__checkAdminToken(jdata)
        if isinstance(ret, dict) and 'result' in ret:
            return ret
        token = ret
        if 'role' not in token or token['role'] != 'admin':
            return self.setError('admin', 'No Permission User')
        userList = self.adminUserRepository.getUserList()
        if userList is None:
            return self.setError('admin', AllError.NoListData)

        return self.setOk('admin', {'userList': userList})

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
            user = self.adminUserRepository.getUserByUserIdPassword(token['userId'], StrUtils.getSha256(jdata['password']))
            if user is None:
                return self.setError('admin', AllError.UnauthorizedUser)
        return token

    def __createAppDatabase(self, scode, jdata):
        if 'host' not in jdata or 'userId' not in jdata or 'password' not in jdata:
            if MultiDbHelper.instance().createDatabaseWithDefault(scode) == False:
                return self.setError('admin', AllError.FailedToCreateDatabase)
            MultiDbHelper.instance().initMysqlWithDefault(scode)
        else:
            if MultiDbHelper.instance().createDatabase(scode, jdata['host'], jdata['port'], jdata['userId'], jdata['password']) == False:
                return self.setError('admin', AllError.FailedToCreateDatabase)
            MultiDbHelper.instance().initMySqlWithDatabase(scode, jdata['host'], jdata['port'], jdata['userId'], jdata['password'], scode)
