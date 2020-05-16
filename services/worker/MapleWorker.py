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
        self.functionMap.update(self.boardCmdAction.funcMap)
        self.functionMap.update(self.channelCmdAction.funcMap)
        self.functionMap.update(self.fileCmdAction.funcMap)
        self.functionMap.update(self.friendCmdAction.funcMap)
        self.functionMap.update(self.messageCmdAction.funcMap)
        
        self.signinToken = SigninToken()

    def work(self, jstr):
        jdata = json.loads(jstr)

        scode = jdata['scode']
        if scode in self.adminFunctionMap:
            self.adminFunctionMap[scode](jdata)
        elif scode in self.userFunctionMap:
            self.userFunctionMap[scode](scode, jdata)
        elif scode in self.appFunctionMap:
            session = self.signinToken.parse(jdata['signinToken'])
            self.appFunctionMap[scode](scode, session, jdata)

    