import requests, json
import logging
import common.config.appconfig as appconfig

from repository.db.IotSmsHistoryRepository import IotSmsHistoryRepository

class SmsManager:
    _instance = None

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._getInstance
        return cls._instance

    def sendSms(self, sensorId, destPhoneNum, textContent):
        headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': appconfig.SMS_AUTH}
        body = {'account': appconfig.SMS_ACCOUNT, 'destPhoneNum': destPhoneNum,
                'srcPhoneNum': appconfig.SMS_NUMBER, 'textContent': textContent, 'ESmsLongTextPolicy': 'SMS_SPLIT_ON_SPACES'}

        res = requests.post(appconfig.SMS_URL, headers = headers, data=json.dumps(body))
        self._saveSmsHistory(sensorId, destPhoneNum, textContent, res)

    def _saveSmsHistory(self, sensorId, destPhoneNum, textContent, res):
        resJson = json.loads(res.text)
        result = resJson['resultCode']
        messageId = resJson['result']['messageIdList'][0]
        IotSmsHistoryRepository().insertSmsHistory(sensorId, destPhoneNum, messageId, result, textContent)

        