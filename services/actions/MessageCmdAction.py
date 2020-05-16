import os, sys, json, datetime
from services.constant.MapleCmd import MapleCmd
from common.utils.StrUtils import StrUtils
from services.constant.AllError import AllError
from services.actions.Action import Action

from repository.db.message.MsgRepository import MsgRepository
from repository.db.message.MsgReadRepository import MsgReadRepository
from repository.db.message.MsgDelRepository import MsgDelRepository
from repository.db.message.MsgDelIdRepository import MsgDelIdRepository
from repository.db.channel.ChannelRepository import ChannelRepository
from repository.db.channel.MyChannelRepository import MyChannelRepository
from repository.db.channel.ChannelLastMsgRepository import ChannelLastMsgRepository

import common.config.appconfig as appconfig

from services.constant.MapleEnum import EMessageType

class MessageCmdAction(Action):
    def __init__(self):
        super().__init__()

        self.mapleCmd = MapleCmd()
        self.msgRepository = MsgRepository()
        self.msgReadRepository = MsgReadRepository()
        self.msgDelRepository = MsgDelRepository()
        self.msgDelIdRepository = MsgDelIdRepository()
        self.channelRepository = ChannelRepository()
        self.myChannelRepository = MyChannelRepository()
        self.channelLastMsgRepository = ChannelLastMsgRepository()

        self.funcMap = {}
        self.funcMap[self.mapleCmd.EMessageCmd().addMessage.name] = lambda scode, session, jdata: self.addMessage(scode, session, jdata)
        self.funcMap[self.mapleCmd.EMessageCmd().syncMessage.name] = lambda scode, session, jdata: self.syncMessage(scode, session, jdata)
        self.funcMap[self.mapleCmd.EMessageCmd().readMessage.name] = lambda scode, session, jdata: self.readMessage(scode, session, jdata)
        self.funcMap[self.mapleCmd.EMessageCmd().delMessage.name] = lambda scode, session, jdata: self.delMessage(scode, session, jdata)


    def addMessage(self, scode, session, jdata):
        userId = session['userId']
        channelId = jdata['channelId']
        msgId = StrUtils.getSha256Uuid('msgId:')

        if self.msgRepository.insert(scode, msgId, channelId, userId, jdata['messageType'], jdata['content']) == False:
            return self.setError(AllError.FailToSaveMessage)
        if self.channelRepository.updateLastMsgAndTime(scode, channelId, self._getShortContent(jdata['content'])) == False:
            return self.setError(AllError.FailToUpdateChannel)
        return self.setOk(scode, {'messageId': msgId, 'content': jdata['content']})

    def syncMessage(self, scode, session, jdata):
        userId = session['userId']
        channelId = jdata['channelId']

        channelRec = self.myChannelRepository.getChannel(scode, userId, channelId)
        if len(channelRec) < 1:
            return self.setError(AllError.NoChannel)
        
        delIdList = self.msgDelIdRepository.getList(scode, channelId, userId, channelRec['createdAt'])
        msgList = None
        if len(delIdList) < 1:
            msgList = self.msgRepository.getMessageListByJoinAt(scode, channelId, channelRec['createdAt'], jdata['offset'], jdata['count'])
        else:
            msgList = self.msgRepository.getMessageListWithoutDeletion(scode, channelId, channelRec['createdAt'], delIdList, jdata['offset'], jdata['count'])
        return self.setOk(scode, {'channelId': channelId, 'messages': msgList})

    def readMessage(self, scode, session, jdata):
        userId = session['userId']
        channelId = jdata['channelId']
        
        channelRec = self.myChannelRepository.getChannel(scode, userId, channelId)
        if len(channelRec) < 1:
            return self.setError(scode, AllError.NoChannel)

        msgList = self.msgRepository.getMessageListByIds(scode, channelId, jdata['messageIds'])
        if len(msgList) < 1:
            return self.setError(scode, AllError.NoMessage)
        
        readIds = []
        for message in msgList:
            messageId = message['messageId']
            self.msgReadRepository.insert(scode, channelId, userId, messageId)
            self.msgRepository.incReadCount(scode, messageId)
            readIds.append(messageId)
        return self.setOk(scode, {'channelId': channelId, 'readIds': readIds})

    def delMessage(self, scode, session, jdata):
        userId = session['userId']
        channelId = jdata['channelId']

        deletedIds = []
        for messageId in jdata['messageIds']:
            if self.msgDelRepository.insert(scode, channelId, userId, messageId) == True:
                deletedIds.append(messageId)
        if len(deletedIds) < 1:
            return self.setError(scode, AllError.FailToDeleteMessage)
        return self.setOk(scode, {'channelId': channelId, 'deletedIds': deletedIds})
