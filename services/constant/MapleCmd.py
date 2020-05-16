from enum import Enum

class MapleCmd:
    mapleCmdHash = {}
    
    def __init__(self):
        self.__makeCmdHash(EAdminCmd)
        self.__makeCmdHash(EBoardCmd)
        self.__makeCmdHash(EChannelCmd)
        self.__makeCmdHash(EFileCmd)
        self.__makeCmdHash(EFriendCmd)
        self.__makeCmdHash(EMessageCmd)
        self.__makeCmdHash(EUserCmd)

    def __makeCmdHash(self, enums):
        for enum in list(enums):
            maplecmdHash[enum.name] = enum

    class EAdminCmd(Enum):
        adminRegister = "adminRegister"
        adminLogin = "adminLogin"
        adminLogout = "adminLogout"
        adminAddApp = "adminAddApp"
        adminDelApp = "adminDelApp"
        adminAppList = "adminAppList"
        adminModifyApp = "adminModifyApp"
        adminAppCount = "adminAppCount"
        adminStopApp = "adminStopApp"
        adminRunApp = "adminRunApp"
        adminReadyApp = "adminReadyApp"        

    class EBoardCmd(Enum):
        addBoard = "addBoard"
        delBoard = "delBoard"
        updateBoardTitle = "updateBoardTitle"
        updateBoardContent = "updateBoardContent"
        updateBoardCategory = "updateBoardCategory"
        updateBoard = "updateBoard"
        getBoardList = "getBoardList"
        getBoardContent = "getBoardContent"
        incBoardLike = "incBoardLike"
        dislike = "incBoardDislike"
        addReply = "addReply"
        delReply = "delReply"
        replyList = "replyList"
        addVote = "addVote"
        voteItemList = "voteItemList"
        selectVoteItem = "selectVoteItem"
        updateVote = "updateVote"
        changeVoteSelection = "changeVoteSelection"
        getVoteInfoList = "getVoteInfoList"

    class EChannelCmd(Enum):
        channelCreate = "channelCreate"
        channelExit = "channelExit"
        chenter = "channelEnter"
        channelInvite = "channelInvite"
        myChannel = "myChannel"
        myChannelCount = "myChannelCount"
        channelLastMessage = "channelLastMessage"
        channelInfos = "channelInfos"

    class EFileCmd(Enum):
        uploadFile = "uploadFile"
        multiUploadFile = "multiUploadFile"
        

    class EFriendCmd(Enum):
        addFriend = "addFriend"
        delFriend = "delFriend"
        changeFriendType = "changeFriendType"
        getFriendList = "getFriendList"
        friendCount = "friendCount"
        friendsInfo = "friendsInfo"
        friendMeUser = "friendMeUser"
        appendMeCount = "appendMeCount"
        blockMeCount = "blockMeCount"

    class EMessageCmd(Enum):
        addMessage = ""
        syncMessage = "syncmsg"
        readMessage = "rcvmsg"
        delMessage = "readmsg"
        online = "online"
        push = "push"

    class EUserCmd(Enum):
        registerIdPw = "registerIdPw"
        registerEmail = "registerEmail"
        registerPhone = "registerPhone"
        userLogin = "userLogin"
        userSignIn = "userSignIn"
        userChangePW = "userChangePW"
        findUserName = "findUserName"
        userChangeEmail = "userChangeEmail"
        userChangePhone = "userChangePhone"
        userVerifyEmail = "userVerifyEmail"
        userVerifySms = "userVerifySms"
        anonymousLogin = "anonymousLogin"
        anonymousSignIn = "anonymousSignIn"
        userFindId = "userFindId"

