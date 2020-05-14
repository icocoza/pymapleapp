import os, sys, json, datetime
from services.constant.MapleCmd import MapleCmd
from common.utils.StrUtils import StrUtils
from services.constant.AllError import AllError
from services.actions.Action import Action

from repository.db.channel.ChannelRepository import ChannelRepository
from repository.db.channel.MyChannelExtRepository import MyChannelExtRepository
from repository.db.channel.MyChannelRepository import MyChannelRepository
from repository.db.channel.ChannelLastMsgRepository import ChannelLastMsgRepository
from services.constant.MapleEnum.EChannelType import EChannelType

class ChannelCmdAction(Action):
    def __init__(self):
        super().__init__()

        self.channelRepository = ChannelRepository()
        self.myChannelRepository = MyChannelRepository()
        self.myChannelExtRepository = MyChannelExtRepository()
        self.channelLastMsgRepository = ChannelLastMsgRepository()
    
    def channelCreate(self, scode, session, jdata):
        userId = session['userId']
        attendeeCount = 2
        if len(jdata['attendees']) > 1:
            jdata['attendees'].append(userId)
            attendeeCount += 1
        else:
            channelRec = self.channelRepository.findChannel(scode, userId, jdata['attendees'][0])
            if channelRec != None:
                self.myChannelRepository.insert(scode, userId, channelRec['channelId'])
                return self.Ok(scode, channelRec['channelId'])
        channelId = StrUtils.getSha256Uuid('channelId:')
        attendees = '|'.join([ attendee for attendee in jdata['attendees']])
        self.channelRepository.insert(scode, channelId, userId, attendees, EChannelType.oneToOne if attendeeCount == 2 else EChannelType.group)
        self.myChannelRepository.insert(scode, userId, channelRec['channelId'])
        return self.Ok(scode, channelRec['channelId'])

    def channelExit(self, scode, session, jdata):
        userId = session['userId']
        channelId = jdata['channelId']

        channelRec = self.channelRepository.getChannel(scode, channelId)
        if channelRec == None:
            return self.setError(scode, AllError.NoChannel)
        
        self.myChannelRepository.delete(scode, userId, channelId)
        if channelRec['channelType'] == EChannelType.group.name():
            attendees = channelRec['attendees']
            if userId in attendees:
                attendees = attendees.replace(userId+'|', '').replace(userId, '')
            if len(attendees) < 1:
                self.channelRepository.delete(scode, channelId)
            else:
                self.channelRepository.updateChatChannelAttendee(scode, channelId, attendees, channelRec['attendeeCount']-1)
        return self.setOk(scode, {'channelId': channelId, 'attendees': attendees.split('|', -1)})

    def channelEnter(self, scode, session, jdata):
        userId = session['userId']
        channelId = jdata['channelId']

        channelRec = self.channelRepository.getChannel(scode, channelId)
        if channelRec == None:
            return self.setError(scode, AllError.NoChannel)
        self.myChannelRepository.insert(scode, userId, channelId)

        return self.setOk(scode, {'channelId': channelId})

    def channelInvite(self, scode, session, jdata):
        userId = session['userId']
        channelId = jdata['channelId']

        channelRec = self.channelRepository.getChannel(scode, channelId)
        if channelRec == None:
            return self.setError(scode, AllError.NoChannel)

        attendees = channelRec['attendees'].split('|', -1)
        attendeeCount = len(attendees)
        for invitee in jdata['invitees']:
            if invitee not in attendees:
                attendees.append(invitee)
        if userId not in attendees:
            attendees.append(userId)
            
        attendeeStr = '|'.join([attendee for attendee in attendees])
        if self.channelRepository.updateAttendee(scode, channelId, attendeeStr, len(attendees), EChannelType.group.name()) == False:
             return self.setError(scode, AllError.FailToUpdate)
        return self.setOk(scode, {'channelId': channelId, 'attendees': attendees})

    def myChannel(self, scode, session, jdata):
        userId = session['userId']
        channelList = self.myChannelRepository.getChannelList(scode, userId, jdata['offset'], jdata['count'])
        if len(channelList) < 1:
            return self.setError(scode, AllError.NoListData)
        return self.setOk(scode, {'channelList': channelList})

    def myChannelCount(self, scode, session, jdata):
        userId = session['userId']
        count = self.myChannelRepository.getChannelCount(scode, userId)
        return self.setOk(scode, {'count': count})

    def channelLastMessage(self, scode, session, jdata):
        userId = session['userId']
        channelList = self.channelLastMsgRepository.getChannelLastMsg(scode, jdata['channelIds'])
        return self.setOk(scode, channelList)

    def channelInfos(self, scode, session, jdata):
        userId = session['userId']
        channelList = self.myChannelExtRepository.getChannelInfoList(scode, userId, jdata['offset'], jdata['count'])
        return self.setOk(scode, channelList)