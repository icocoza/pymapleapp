import os, sys, json, datetime, time
import hashlib
from services.constant.MapleCmd import EUserCmd
import common.utils.StrUtils as StrUtils
from services.constant.AllError import AllError
from services.actions.Action import Action
from services.actions.user.LoginToken import LoginToken
from services.actions.user.SigninToken import SigninToken
from services.actions.user.AppToken import AppToken
from services.constant.MapleEnum import EUserAuthType

from repository.db.user.UserRepository import UserRepository
from repository.db.user.UserAuthRepository import UserAuthRepository
from repository.db.user.UserPushRepository import UserPushRepository
from repository.db.user.UserTokenRepository import UserTokenRepository


class UserCmdAction(Action):
    def __init__(self):
        super().__init__()

        self.loginToken = LoginToken()
        self.signinToken = SigninToken()
        self.appToken = AppToken()

        self.userRepository = UserRepository()
        self.userAuthRepository = UserAuthRepository()
        self.userPushRepository = UserPushRepository()
        self.userTokenRepository = UserTokenRepository()

        self.funcMap = {}
        self.funcMap[EUserCmd.registerIdPw.name] = lambda scode, jdata: self.registerIdPw(scode, jdata)
        self.funcMap[EUserCmd.registerEmail.name] = lambda scode, jdata: self.registerEmail(scode, jdata)
        self.funcMap[EUserCmd.registerPhone.name] = lambda scode, jdata: self.registerMobile(scode, jdata)
        self.funcMap[EUserCmd.userLogin.name] = lambda scode, jdata: self.userLogin(scode, jdata)
        self.funcMap[EUserCmd.anonymousLogin.name] = lambda scode, jdata: self.anonymousLogin(scode, jdata)
        self.funcMap[EUserCmd.userSignIn.name] = lambda scode, jdata: self.userSignIn(scode, jdata)
        self.funcMap[EUserCmd.userChangePW.name] = lambda scode, jdata: self.userChangePW(scode, jdata)
        self.funcMap[EUserCmd.findUserName.name] = lambda scode, jdata: self.findUserName(scode, jdata)

    def __registerUser(self, scode, authType, jdata, enableToken):
        userId = jdata['userId'] if 'userId' in jdata else StrUtils.getMapleUuid('userId:') #for anonymous user

        authQuery = None
        if authType == EUserAuthType.idpw:
            authQuery = self.userAuthRepository.qInsertUserNamePw(scode, userId, jdata['userName'], jdata['password'])
        elif authType == EUserAuthType.email:
            authQuery = self.userAuthRepository.qInsertEmail(scode, userId, jdata['email'])
        elif  authType == EUserAuthType.mobile:
            self.userAuthRepository.qInsertPhoneNo(scode, userId, jdata['mobileNo'])
        if authQuery == None:
            return self.setError(scode, AllError.UnknownAuthType)
        tokenId, token = self.loginToken.create(scode, userId, jdata['uuid'], authType)
        queries = []
        if authQuery is not None:
            queries.append(authQuery)
        if 'userName' not in jdata:
            jdata['userName'] = 'No.' + str(int(round(time.time() * 1000)))

        queries.append(self.userRepository.qInsert(scode, userId, jdata['userName'], authQuery==None))
        
        queries.append(self.userTokenRepository.qInsertToken(scode, userId, jdata['uuid'], tokenId, token, enableToken))
        if self.userRepository.multiQueries(scode, queries) == False:
            return self.setError(scode, AllError.FailedUserRegister)
        return self.setOk(scode, {'loginToken': token})
    
    def registerIdPw(self, scode, jdata):
        if len(jdata['userName']) < 6:
            return self.setError(scode, AllError.userIdMoreThan6Characters)
        if len(jdata['password']) < 8:
            return self.setError(scode, AllError.passwordMoreThan8Characters)
        if 'appToken' not in jdata or len(jdata['appToken']) < 1:
            return self.setError(scode, AllError.appTokenNotExist)
        
        appId, scode = self.appToken.parseApp(jdata['appToken'])
        err = self.appToken.checkScode(scode)
        if err != AllError.ok:
            return self.setError(scode, err)
        if self.userAuthRepository.findUserName(scode, jdata['userName']):
            return self.setError(scode, AllError.ExistUserName)
        return self.__registerUser(scode, EUserAuthType.idpw, jdata, False)

    def registerEmail(self, scode, jdata):
        if StrUtils.isEmail(jdata['email']):
            return self.setError(scode, AllError.InvalidEmailFormat)
        appId, scode = self.appToken.parseApp(jdata['appToken'])
        err = self.appToken.checkScode(scode)
        if err != AllError.ok:
            return self.setError(scode, err)
        if self.userAuthRepository.findEmail(scode, jdata['email']):
            return self.setError(scode, AllError.ExistEmail)
        return self.__registerUser(scode, EUserAuthType.email, jdata, False)

    def registerMobile(self, scode, jdata):
        if StrUtils.isPhone(jdata['mobile']):
            return self.setError(scode, AllError.InvalidMobileFormat)
        appId, scode = self.appToken.parseApp(jdata['appToken'])
        err = self.appToken.checkScode(scode)
        if err != AllError.ok:
            return self.setError(scode, err)

        if self.userAuthRepository.findMobile(scode, jdata['mobile']):
            return self.setError(scode, AllError.ExistPhoneNo)
        return self.__registerUser(scode, EUserAuthType.mobile, jdata, False)

    def userLogin(self, scode, jdata):
        appId, scode = self.appToken.parseApp(jdata['appToken'])

        auth = self.userAuthRepository.getUserByUserName(scode, jdata['userName'])
        if auth == None:
            return self.setError(scode, AllError.NotExistUserAuth)

        if EUserAuthType(auth['authType']) == EUserAuthType.idpw and auth['password'] != StrUtils.getSha256(jdata['password']):
            return self.setError(scode, AllError.InvalidUser)
        
        userId = auth['userId']
        uuid = jdata['uuid']
        tokenRec = self.userTokenRepository.getTokenByUserId(scode, userId)
        if tokenRec == None:
            return self.setError(scode, AllError.UnauthorizedUserId)

        tokenId, token = self.loginToken.create(scode, userId, uuid, auth['authType'])  #로그인하면 로그인토큰을 매번 갱신한다.
        result = False
        if tokenRec['uuid'] == uuid:
            result = self.userTokenRepository.updateToken(scode, userId, uuid, tokenId, token, True)
        else:
            queries = []
            queries.append(self.userTokenRepository.qDeleteTokenByUuid(scode, userId, uuid))
            queries.append(self.userTokenRepository.qInsertToken(scode, userId, uuid, tokenId, token, True))
            result = self.userRepository.multiQueries(scode, queries)
        if result == False:
            return self.setError(scode, AllError.FailedUpdateToken)
        
        self.userPushRepository.insert(scode, userId, uuid, jdata['epid'] if 'epid' in jdata else '')
        self.userRepository.updateUserDetail(scode, userId, 
                jdata['osType'] if 'osType' in jdata else '', 
                jdata['osVersion'] if 'osVersion' in jdata else '', 
                jdata['appVersion']if 'appVersion' in jdata else '')
        return self.setOk(scode, {'loginToken': token})

    def anonymousLogin(self, scode, jdata):
        appId, scode = self.appToken.parseApp(jdata['appToken'])

        if self.userRepository.findUserName(scode, jdata['userName']) == True:
            return self.setError(scode, AllError.ExistUserName)

        userId = StrUtils.getMapleUuid('anonymous:')
        jdata['userId'] = userId
        jdata['password'] = jdata['userName'] + '!@#$'

        ret = self.registerIdPw(scode, jdata)
        if ret['result'] == 'error':
            return ret
        
        auth = self.userAuthRepository.getUserByUserName(scode, jdata['userName'])
        if auth == None:
            return self.setError(scode, AllError.FailToCreateAnonymousAccount)
        
        tokenRec = self.userTokenRepository.getTokenByUserId(scode, userId)
        if tokenRec == None:
            return self.setError(scode, AllError.UnauthorizedAnonymousUserId)
        
        self.userPushRepository.insert(scode, userId, tokenRec['uuid'], jdata['epid'] if 'epid' in jdata else '')
        self.userRepository.updateUserDetail(scode, userId, 
                jdata['osType'] if 'osType' in jdata else '', 
                jdata['osVersion'] if 'osVersion' in jdata else '', 
                jdata['appVersion']if 'appVersion' in jdata else '')
        return self.setOk(scode, {'loginToken': tokenRec['token']})

    def userSignIn(self, scode, jdata):
        token = self.loginToken.parse(jdata['loginToken'])
        if token == None:
            return self.setError(scode, AllError.InvalidLoginToken)
        if token['uuid'] != jdata['uuid']:
            return self.setError(scode, AllError.InvalidUUID)

        userId = token['userId']
        tokenRec = self.userTokenRepository.getToken(token['scode'], userId, token['uuid'])
        if tokenRec == None or jdata['loginToken'] != tokenRec['token']:
            return self.setError(scode, AllError.ExpiredOrDifferentLoginToken)
        
        authRec = self.userAuthRepository.getUser(token['scode'], userId)
        if authRec == None:
            return self.setError(scode, AllError.MightBeLeftUser)
        userRec = self.userRepository.getUser(token['scode'], userId)
        if userRec == None:
            return self.setError(scode, AllError.MightBeLeftUser)

        signinTokenId, signinToken = self.signinToken.create(scode, userId, authRec['userName'], token['uuid'], tokenRec['tokenId'])
        self.userRepository.updateLastVisit(scode, userId)

        return self.setOk(scode, {'signinToken': signinToken, 'lastAt': userRec['lastAt'], 'userName': userRec['userName']})

    def userChangePW(self, scode, jdata):
        token = self.signinToken.parse(jdata['signinToken'])
        if token is None or token['scode'] != scode:
            return self.setError(scode, AllError.InvalidSigninToken)

        if self.signinToken.isExpired(token['startAt']):
            return self.setError(scode, AllError.ExpiredSigninToken)
        if 'password' not in jdata:
            return self.setError(scode, AllError.EmptyOldPassword)
        if len(jdata['newpw'])<8:
            return self.setError(scode, AllError.passwordMoreThan8Characters)

        oldPasswd = hashlib.sha256(jdata['password'].encode()).hexdigest()
        newPasswd = hashlib.sha256(jdata['newpw'].encode()).hexdigest()

        authRec = self.userAuthRepository.getUser(scode, token['userId'])
        if authRec == None:
            return self.setError(scode, AllError.MightBeLeftUser)
        if authRec['password'] != oldPasswd:
            return self.setError(scode, AllError.MismatchOldPassword)
        if authRec['password'] == jdata['newpw']:
            return self.setError(scode, AllError.SameWithOldPassword)
        if self.userAuthRepository.updatePw(scode, token['userId'], jdata['newpw']) == False:
            return self.setError(scode, AllError.FailToChangePW)
        return self.setOk(scode, "Success")

    def findUserName(self, scode, jdata):
        if len(jdata['userName']) < 6:
            return self.setError(scode, AllError.userIdMoreThan6Characters)
        appId, scode = self.appToken.parseApp(jdata['appToken'])
        err = self.appToken.checkScode(scode)
        if err != AllError.ok:
            return self.setError(scode, err)
        userRec = self.userRepository.findUserName(scode, jdata['userName'])
        if userRec is None:
            return self.setError(scode, AllError.NotExistUserId)
        return self.setOk(scode, 'Exist')

    def userChangeEmail(self, scode, jdata):
        return self.setError(scode, AllError.NotImplemented)

    def userChangeMobile(self, scode, jdata):
        return self.setError(scode, AllError.NotImplemented)

    def userVerifyEmail(self, scode, jdata):
        return self.setError(scode, AllError.NotImplemented)

    def userVerifySms(self, scode, jdata):
        return self.setError(scode, AllError.NotImplemented)

    def userChangeEmail(self, scode, jdata):
        return self.setError(scode, AllError.NotImplemented)
