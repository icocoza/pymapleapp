import re 
import hashlib, uuid
import time 

def __isPattern(pattern, data):
    if(re.search(pattern, data)):
        return True
    return False

EMAIL_PATTERN = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
EMAIL_PATTERN2 = '^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$'
def isEmail(data):
    return __isPattern(EMAIL_PATTERN2, data)

PHONE_PATTERN = "^\\(?(\\d{3})\\)?[- ]?(\\d{3,4})[- ]?(\\d{4})$"
def isPhone(data):
    return __isPattern(PHONE_PATTERN, data)

ALPHA_NUMERIC_PATTERN = "((?<=[a-zA-Z])(?=[0-9]))|((?<=[0-9])(?=[a-zA-Z]))"
def isAlphaNumeric(data):
    return __isPattern(ALPHA_NUMERIC_PATTERN, data)

KOREAN_NUMERIC_PATTERN = "((?<=[ㄱ-ㅎ가-힣])(?=[0-9]))|((?<=[0-9])(?=[ㄱ-ㅎ가-힣]))"
def isKoreanNumeric(data):
    return __isPattern(KOREAN_NUMERIC_PATTERN, data)

NUMERIC_DASH_PATTERN = "[0-9][0-9-]*[0-9]"
def isNumericDash(data):
    return __isPattern(NUMERIC_DASH_PATTERN, data)

NUMERIC_PATTERN = "[0-9]"
def isNumeric(data):
    return __isPattern(NUMERIC_PATTERN, data)

IMAGE_PATTERN = "([^\\s]+(\\.(?i)(jpg|png|gif|bmp|jpeg))$)"
def isImageFile(data):
    return __isPattern(IMAGE_PATTERN, data)

URL_PATTERN = "\\(?\\b((http|https)://|www[.])[-A-Za-z0-9+&amp;@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&amp;@#/%=~_()|]"
def isUrl(data):
    return __isPattern(URL_PATTERN, data)

FILENAME_PATTER = "^[A-Za-z0-9-_,\\s]+[.]{1}[A-Za-z]{3}$"
def isFilename(data):
    return __isPattern(FILENAME_PATTER, data)

def extractUrls(text):
    return re.findall(r'(https?://\S+)', text)

def getMapleUuid(prefix):
    return prefix + hashlib.sha1(str(uuid.uuid1()).encode()).hexdigest() + str(int(round(time.time() * 1000)))

def getSha256(data):
    return hashlib.sha256(data.encode()).hexdigest()