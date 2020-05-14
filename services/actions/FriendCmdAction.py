import os, sys, json, datetime
from services.constant.MapleCmd import MapleCmd
from common.utils.StrUtils import StrUtils
from services.constant.AllError import AllError
from services.actions.Action import Action

from repository.db.friend.FriendRepository import FriendRepository
from repository.db.friend.FriendInfoRepository import FriendInfoRepository
import common.config.appconfig as appconfig

from services.constant.MapleEnum.EFriendType import EFriendType
from services.constant.MapleEnum.EFriendStatus import EFriendStatus

class FriendCmdAction(Action):
    def __init__(self):
        super().__init__()

        self.friendRepository = FriendRepository()
        self.friendInfoRepository = FriendInfoRepository()

    def addFriend(self, scode, session, jdata):
        userId = session['userId']
        friendList = jdata['friendList']

        addedFriend = []
        for friend in friendList:
            if self.friendRepository.insert(scode, userId, friend['friendId'], friend['friendName'], jdata['friendType']) == True:
                addedFriend.append({'friendId': friend['friendId'], 'friendName': friend['friendName']})
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

        for friend in jdata['friendList']:
            if self.friendRepository.updateFriendType(scode, userId, friend['friendId'], friend['friendType']) == True:
                updatedFriend.append(friend['friendId'])
        return self.setOk(scode, {'updated': updatedFriend})

    def changeFriendType(self, scode, session, jdata):
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
        count = self.friendRepository.getFriendMeCount(scode, userId, EFriendType.block.name())
        return self.setOk(scode, {'count': count})
