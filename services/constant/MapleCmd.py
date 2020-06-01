from enum import Enum

class EAdminCmd(Enum):
    adminAdminRegister = "adminAdminRegister"
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
    adminUserList = "adminUserList"

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
    incBoardDislike = "incBoardDislike"
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
    channelEnter = "channelEnter"
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
    syncMessage = "syncMessage"
    readMessage = "readMessage"
    delMessage = "delMessage"
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

