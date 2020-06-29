import os, sys, json, datetime
from services.constant.MapleCmd import EFriendCmd
import common.utils.StrUtils as StrUtils
from services.constant.AllError import AllError
from services.actions.Action import Action

from repository.db.friend.FriendRepository import FriendRepository
from repository.db.friend.FriendInfoRepository import FriendInfoRepository
from repository.db.user.UserRepository import UserRepository
import common.config.appconfig as appconfig

from services.constant.MapleEnum import EFriendType
from services.constant.MapleEnum import EFriendStatus

class FriendCmdAction(Action):
    def __init__(self):
        super().__init__()

        self.friendRepository = FriendRepository()
        self.friendInfoRepository = FriendInfoRepository()
        self.userRepository = UserRepository()

        self.funcMap = {}
        self.funcMap[EFriendCmd.addFriend.name] = lambda scode, session, jdata: self.addFriend(scode, session, jdata)
        self.funcMap[EFriendCmd.delFriend.name] = lambda scode, session, jdata: self.delFriend(scode, session, jdata)
        self.funcMap[EFriendCmd.changeFriendType.name] = lambda scode, session, jdata: self.changeFriendType(scode, session, jdata)
        self.funcMap[EFriendCmd.getFriendList.name] = lambda scode, session, jdata: self.getFriendList(scode, session, jdata)
        
        self.funcMap[EFriendCmd.friendCount.name] = lambda scode, session, jdata: self.friendCount(scode, session, jdata)
        self.funcMap[EFriendCmd.friendsInfo.name] = lambda scode, session, jdata: self.friendsInfo(scode, session, jdata)
        self.funcMap[EFriendCmd.friendMeUser.name] = lambda scode, session, jdata: self.friendMeUser(scode, session, jdata)
        self.funcMap[EFriendCmd.appendMeCount.name] = lambda scode, session, jdata: self.appendMeCount(scode, session, jdata)
        self.funcMap[EFriendCmd.blockMeCount.name] = lambda scode, session, jdata: self.blockMeCount(scode, session, jdata)

    def addFriend(self, scode, session, jdata):
        userId = session['userId']
        friendIds = jdata['friendIds']

        addedFriend = []
        friendList = self.userRepository.getUserList(scode, friendIds)
        if len(friendList) < 1:
            return self.setError(scode, AllError.NoFriendInfo)
        for friendId in friendIds:
            if friendId in friendList:
                if self.friendRepository.insert(scode, userId, friendId, friendList[friendId], EFriendType.friend.name) == True:
                    addedFriend.append({'friendId': friendId, 'friendName': friendList[friendId]})
        return self.setOk(scode, {'added': addedFriend})

    def delFriend(self, scode, session, jdata):
        userId = session['userId']
        friendIds = jdata['friendIds']

        deletedFriend = []
        for friendId in friendIds:
            if self.friendRepository.delete(scode, userId, friendId) == True:
                deletedFriend.append(friendId)
        return self.setOk(scode, {'deleted': deletedFriend})

    def changeFriendType(self, scode, session, jdata):
        userId = session['userId']
        updatedFriend = []

        for friendId in jdata['friendIds']:
            if self.friendRepository.updateFriendType(scode, userId, friendId, jdata['friendType']) == True:
                updatedFriend.append(friendId)
        return self.setOk(scode, {'updated': updatedFriend, 'friendType': jdata['friendType']})

    def getFriendList(self, scode, session, jdata):
        userId = session['userId']
        friendList = self.friendRepository.getListByType(scode, userId, jdata['friendType'], jdata['offset'], jdata['count'])
        if len(friendList) < 1:
            return self.setError(scode, AllError.NoListData)
        return self.setOk(scode, friendList)

    def friendCount(self, scode, session, jdata):
        userId = session['userId']
        count = self.friendRepository.getCount(scode, userId, jdata['friendType'])
        return self.setOk(scode, {'friendType': jdata['friendType'], 'count': count})

    def friendsInfo(self, scode, session, jdata):
        userId = session['userId']
        friendInfoList = self.friendRepository.getListByIds(scode, userId, jdata['friendIds'])
        if len(friendInfoList) < 1: 
            return self.setError(scode, AllError.NoListData)
        return self.setOk(scode, friendInfoList)

    def friendMeUser(self, scode, session, jdata):
        userId = session['userId']
        friendInfoList = self.friendRepository.getFriendMeList(scode, userId, jdata['friendType'], jdata['offset'], jdata['count'])
        if len(friendInfoList) < 1: 
            return self.setError(scode, AllError.NoListData)
        return self.setOk(scode, friendInfoList)

    def appendMeCount(self, scode, session, jdata):
        userId = session['userId']
        count = self.friendRepository.getFriendMeCount(scode, userId, jdata['friendType'])
        return self.setOk(scode, {'count': count})

    def blockMeCount(self, scode, session, jdata):
        userId = session['userId']
        count = self.friendRepository.getFriendMeCount(scode, userId, EFriendType.block.name)
        return self.setOk(scode, {'count': count})
