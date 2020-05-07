from enum import Enum

class EUserRole(Enum):
    user = "user"
    adminUser = "adminUser"
    adminMaster = "adminMaster"
    anonymous = "anonymous"

class EAdminAppStatus(Enum):
    ready = "ready"
    block = "block"
    deleted = "deleted"
    pending = "pending"
    stop = "stop"
    all = "all"

class EAdminStatus(Enum):
    normal = "normal"
    pending = "pending"
    reject = "reject"
    block = "block"
    leave = "leave"


class EAuthProvider(Enum):
    local = "local"
    facebook = "facebook"
    google = "google"
    github = "github"

class EMessageType(Enum):
    chat = "chat"
    online = "online"
    push = "push"

class EUploadFileType(Enum):
    png = "png"
    jpg = "jpg"
    gif = "gif"


class EUserAuthType(Enum):
    idpw = "idpw"
    email = "email"
    mobile = "mobile"
    quit = "quit"
    none = "none"

class EFriendStatus(Enum):
    normal = "normal"
    busy = "busy"
    offline = "offline"
    leave = "leave"

class EFriendType(Enum):
    friend = "friend"
    block = "block"
    black = "black"
    unknown = "unknown"
    all = "all"

class EChannelType(Enum):
    oneToOne = "oneToOne"
    group = "group"
    openChannel = "openChannel"


class EBoardContentType(Enum):
    text = "text"
    json = "json"
    image = "image"
    vote = "vote"
    audio = "audio"
    video = "video"
    link = "link"

class EBoardPreferences(Enum):
    like = "like"
    dislike = "dislike"
    happy = "happy"
    smile = "smile"
    sad = "sad"
