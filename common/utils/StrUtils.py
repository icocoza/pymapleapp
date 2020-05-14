import re 
import hashlib, uuid

class StrUtils:

    def __isPattern(self, pattern, data):
        if(re.search(pattern, data)):
            return True
        return False

    EMAIL_PATTERN = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    EMAIL_PATTERN2 = '^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$'
    def isEmail(self, data):
        return self.__isPattern(EMAIL_PATTERN2, data)

    PHONE_PATTERN = "^\\(?(\\d{3})\\)?[- ]?(\\d{3,4})[- ]?(\\d{4})$"
    def isPhone(self, data):
        return self.__isPattern(PHONE_PATTERN, data)

    ALPHA_NUMERIC_PATTERN = "((?<=[a-zA-Z])(?=[0-9]))|((?<=[0-9])(?=[a-zA-Z]))"
    def isAlphaNumeric(self, data):
        return self.__isPattern(ALPHA_NUMERIC_PATTERN, data)

    KOREAN_NUMERIC_PATTERN = "((?<=[ㄱ-ㅎ가-힣])(?=[0-9]))|((?<=[0-9])(?=[ㄱ-ㅎ가-힣]))"
    def isKoreanNumeric(self, data):
        return self.__isPattern(KOREAN_NUMERIC_PATTERN, data)

    NUMERIC_DASH_PATTERN = "[0-9][0-9-]*[0-9]"
    def isNumericDash(self, data):
        return self.__isPattern(NUMERIC_DASH_PATTERN, data)

    NUMERIC_PATTERN = "[0-9]"
    def isNumeric(self, data):
        return self.__isPattern(NUMERIC_PATTERN, data)

    IMAGE_PATTERN = "([^\\s]+(\\.(?i)(jpg|png|gif|bmp|jpeg))$)"
    def isImageFile(self, data):
        return self.__isPattern(IMAGE_PATTERN, data)

    URL_PATTERN = "\\(?\\b((http|https)://|www[.])[-A-Za-z0-9+&amp;@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&amp;@#/%=~_()|]"
    def isUrl(self, data):
        return self.__isPattern(URL_PATTERN, data)

    FILENAME_PATTER = "^[A-Za-z0-9-_,\\s]+[.]{1}[A-Za-z]{3}$"
    def isFilename(self, data):
        return self.__isPattern(FILENAME_PATTER, data)

    def extractUrls(self, text):
        return re.findall(r'(https?://\S+)', text)

    def getSha256Uuid(self, prefix):
        return prefix + hashlib.sha256(uuid.uuid1().hex().encode()).hexdigest()
    
    def getSha256(self, data):
        return hashlib.sha256(data.encode()).hexdigest()