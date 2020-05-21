import os, sys, json, datetime

from services.actions.AdminCmdAction import AdminCmdAction
from services.actions.BoardCmdAction import BoardCmdAction
from services.actions.ChannelCmdAction import ChannelCmdAction
from services.actions.FileCmdAction import FileCmdAction
from services.actions.FriendCmdAction import FriendCmdAction
from services.actions.MessageCmdAction import MessageCmdAction
from services.actions.UserCmdAction import UserCmdAction

from services.actions.user.SigninToken import SigninToken

class MapleWorker:

    def __init__(self):
        super().__init__()

        self.adminCmdAction = AdminCmdAction()
        self.boardCmdAction = BoardCmdAction()
        self.channelCmdAction = ChannelCmdAction()
        self.fileCmdAction = FileCmdAction()
        self.friendCmdAction = FriendCmdAction()
        self.messageCmdAction = MessageCmdAction()
        self.userCmdAction = UserCmdAction()

        self.adminFunctionMap = {}
        self.adminFunctionMap.update(self.adminCmdAction.funcMap)

        self.userFunctionMap = {}
        self.userFunctionMap.update(self.userCmdAction.funcMap)
        
        self.appFunctionMap = {}
        self.appFunctionMap.update(self.boardCmdAction.funcMap)
        self.appFunctionMap.update(self.channelCmdAction.funcMap)
        self.appFunctionMap.update(self.fileCmdAction.funcMap)
        self.appFunctionMap.update(self.friendCmdAction.funcMap)
        self.appFunctionMap.update(self.messageCmdAction.funcMap)
        
        self.signinToken = SigninToken()

    def work(self, jstr):
        jsonobj = json.loads(jstr)
        self.workJson(jsonobj['scode'], jsonobj['data'])

    def workJson(self, jdata):
        scode = jdata['scode']
        data = jdata['data']
        cmd = data['cmd']
        #TODO this needs to check the api-key
        if cmd in self.adminFunctionMap:
            return self.adminFunctionMap[cmd](data)
        elif cmd in self.userFunctionMap:
            return self.userFunctionMap[cmd](scode, data)
        elif cmd in self.appFunctionMap:
            session = self.signinToken.parse(data['signinToken'])
            return self.appFunctionMap[cmd](scode, session, data)
        return None