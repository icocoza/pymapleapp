
from datetime import datetime, timedelta
import logging 
from repository.db.AirKoreaQualityRepository import AirKoreaQualityRepository

class AirKorManager:
    _instance = None

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._getInstance
        return cls._instance

    def __init__(self):
        self.airKoreaQualityRepository = AirKoreaQualityRepository()
        self.airQualityMap = {}   #메타정보를 캐싱함
        pass

    def getAirQuality(self, sido, gugun):
        key = sido + '-' + gugun
        if key in self.airQualityMap:
            record = self.airQualityMap[key]
            sensorAt = datetime.strptime(record['sensorAt'].strftime('%Y-%m-%d %H:00:00'), '%Y-%m-%d %H:00:00')
            if sensorAt > datetime.now() - timedelta(minutes=90):
                return record
        airQuality = self.airKoreaQualityRepository.selectBySidoAndGuGun(sido, gugun)
        if len(airQuality) > 0:            
            self.airQualityMap[key] = airQuality[0]
            return airQuality[0]
        return None

    def getAirQualityBySensorAt(self, sido, gugun, sensorAt):
        sensorAt = sensorAt - timedelta(minutes=30)
        sensorAt = sensorAt.strftime('%Y-%m-%d %H:00:00')
        key = sido + '-' + gugun
        if key in self.airQualityMap:
            record = self.airQualityMap[key]
            if sensorAt == record['sensorAt']:
                return record
        airQuality = self.airKoreaQualityRepository.selectBySensorAtAndCity(sido, gugun, sensorAt)
        if len(airQuality) > 0:
            self.airQualityMap[key] = airQuality[0]
            return airQuality[0]
        return None
         
