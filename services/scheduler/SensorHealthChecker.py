
import logging
import datetime
import time
import schedule
import threading

from module.redis.RedisManager import RedisManager
from module.sms.SmsManager import SmsManager

from repository.db.IotCycleRepository import IotCycleRepository
from repository.db.IotCycleSmsRepository import IotCycleSmsRepository


class SensorHealthChecker:
    
    def __init__(self):
        self.sensorInfos = {}
        self.smsUsers = {}
        self.threading = True
        self.updateMobileNo = 0

        self.doJobLoadSensorIdList()

        schedule.every().minutes.do(self.doJobLoadUnHealthySensor)
        schedule.every(5).minutes.do(self.doJobLoadSensorIdList)

        t = threading.Thread(target=self._threadSchedulerFunc)
        t.start()
        pass

    def stop(self):
        self.threading = False
        pass

    def doJobLoadSensorIdList(self):  #잦은 DB 접근을 방지하기 위해 5분마다 센서ID 업데이트 하도록 함
        self.sensorInfos.clear()
        sensors = IotCycleRepository().selectCycleAll()
        for sensor in sensors:
            self.sensorInfos[sensor['sensorId']] = sensor 
        pass

    def doJobLoadUnHealthySensor(self):        
        # if self.updateMobileNo % 5 == 0: #doJobLoadSensorIdList()
        #     self.doJobLoadSensorIdList()

        for sensorId in self.sensorInfos:
            scode = RedisManager.instance().get('aliveCheck:' + sensorId)
            if scode is None:   #if sensor's ttl is expired, send sms
                self._checkSmsType(self.sensorInfos[sensorId], scode)  #value is scode
        # self.updateMobileNo += 1
        pass

    def _checkSmsType(self, sensor, scode):
        users = IotCycleSmsRepository().selectUserBySensorId(sensor['sensorId'])
        for user in users:
            self._sendSms(sensor['sensorId'], sensor['minutes'], user['mobileNo'])
        uses = IotCycleSmsRepository().selectUserByScode(scode)
        for user in users:
            self._sendSms(sensor['sensorId'], sensor['minutes'], user['mobileNo'])
        pass

    def _sendSms(self, sensorId, minutes, mobileNo):
        value = RedisManager.instance().get('sentSms:' + sensorId)
        if value is not None:
            logging.info(f'{sensorId} - already Sent SMS in 30 Minutes.')
            return
        msg = f'[SKP]센서 {sensorId} 에 지정된 {minutes}분 주기를 초과해 센서 응답이 없습니다.'
        SmsManager.instance().sendSms(sensorId, mobileNo, msg)
        RedisManager.instance().setTtl('sentSms:' + sensorId, msg, 30 * 60) #30분내 다시 보내지 않음
        pass

    def _threadSchedulerFunc(self):
        logging.info('_threadSchedulerFunc()')
        while self.threading:
            schedule.run_pending()
            time.sleep(5)