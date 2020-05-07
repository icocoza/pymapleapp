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
        getcategorylist = "getcategorylist"
        addboard = "addboard"
        delboard = "delboard"
        updatetitle = "updatetitle"
        updatecontent = "updatecontent"
        updatecategory = "updatecategory"
        updateboard = "updateboard"
        boardlist = "boardlist"
        getcontent = "getcontent"
        like = "like"
        dislike = "dislike"
        addreply = "addreply"
        delreply = "delreply"
        replylist = "replylist"
        addvote = "addvote"
        selvote = "selvote"
        voteitemlist = "voteitemlist"
        voteupdate = "voteupdate"
        changeselection = "changeselection"
        voteinfolist = "voteinfolist"
        boardsearch = "boardsearch"        

    class EChannelCmd(Enum):
        chcreate = "chcreate"
        chexit = "chexit"
        chenter = "chenter"
        chinvite = "chinvite"
        chmime = "chmime"
        chcount = "chcount"
        chlastmsg = "chlastmsg"
        chinfo = "chinfo"

    class EFileCmd(Enum):
        uploadFile = "uploadFile"
        multiUploadFile = "multiUploadFile"
        

    class EFriendCmd(Enum):
        addfriend = "addfriend"
        delfriend = "delfriend"
        changefriendstatus = "changefriendstatus"
        friendids = "friendids"
        friendcnt = "friendcnt"
        friendinfos = "friendinfos"
        appendme = "appendme"
        blockme = "blockme"
        appendmecnt = "appendmecnt"
        blockmecnt = "blockmecnt"


    class EMessageCmd(Enum):
        msg = "msg"
        syncmsg = "syncmsg"
        rcvmsg = "rcvmsg"
        readmsg = "readmsg"
        delmsg = "delmsg"
        online = "online"
        push = "push"

    class EUserCmd(Enum):
        registerIdPw = "registerIdPw"
        registerEmail = "registerEmail"
        registerPhone = "registerPhone"
        userLogin = "userLogin"
        userSignIn = "userSignIn"
        userChangePW = "userChangePW"
        userChangeEmail = "userChangeEmail"
        userChangePhone = "userChangePhone"
        userVerifyEmail = "userVerifyEmail"
        userVerifySms = "userVerifySms"
        anonymousLogin = "anonymousLogin"
        anonymousSignIn = "anonymousSignIn"
        userFindId = "userFindId"

