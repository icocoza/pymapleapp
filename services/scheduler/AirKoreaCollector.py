#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import time, sys
import requests, json
import threading
import logging
from datetime import datetime, timedelta
import linecache

from apscheduler.schedulers.background import BackgroundScheduler

import common.config.appconfig as appconfig

from repository.db.AirKoreaQualityRepository import AirKoreaQualityRepository
from module.db.DbHelper import DbHelper
from common.inf.DbConnectionListener import DbConnectionListener
from common.utils.EventHook import EventHook
import common.utils.ExceptionUtil as exutil


class AirKoreaCollector(DbConnectionListener):

    def __init__(self):
        logging.info('AirKoreaCollector Initialized!')
        self.onEventDbConnect = EventHook()
        self.onEventDbConnect += self.onDbConnected
        self.onEventDbError = EventHook()
        self.onEventDbError += self.onDbError
        self.onEventDbDisconnect = EventHook()
        self.onEventDbDisconnect += self.onDbDisconnected
        DbHelper().initMysqlWithDefault(self)
        DbHelper().initSqlAlchemyWithDefault(self)

        self.sidoList = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주", "세종"]
        self.numOfRows = 150
        self.ver = 1.3

        self.airKoreaQualityRepository = AirKoreaQualityRepository()
        pass
    
    def start(self):
        logging.info('AirKoreaCollector Start!')
        self.threading = True
        self.thd = threading.Thread(target=self.holdInstanceUsingThread)
        self.thd.start()
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.doJobLoadAirKoreaList, 'cron', minute='30', id="doJobLoadAirKoreaList") #매시 30분마다 실행
        self.scheduler.start()
        self.doJobLoadAirKoreaList()
        pass

    def stop(self):
        self.threading = False
        self.stop()
        pass

    def doJobLoadAirKoreaList(self):
        logging.info('AirKoreaCollector Start a Job')
        sensorAt = datetime.now().strftime("%Y-%m-%d %H:00:00")
        if self.airKoreaQualityRepository.isExistSensorAt(sensorAt) == True:    #sensorAt 데이터가 있으면 실행하지 않음
            return
        for sido in self.sidoList:
            try:
                url = f'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey={appconfig.airkorea_apikey}&numOfRows={self.numOfRows}&pageNo=1&sidoName={sido}&ver={self.ver}&_returnType=json'
                resp = requests.get(url)
                body = resp.content.decode('utf-8')
                self._insertAirKoreaQuality(sido, body)
            except Exception as ex:
                exutil.PrintException()
        pass
    
    def _insertAirKoreaQuality(self, sido, body):
        try:
            jobj = json.loads(body)
            items = jobj['list']    #json array
            for item in items:
                #sido, gugun, sensorAt, so2, co, o3, no2, pm10, pm25, khai, khaiGrade, so2Grade, coGrade, o3Grade, no2Grade, pm10Grade, pm25Grade
                self.airKoreaQualityRepository.insertAirQuality(sido, item['stationName'], item['dataTime']+':00', item['so2Value'], item['coValue'], 
                    item['o3Value'], item['no2Value'], item['pm10Value'], item['pm25Value'], item['khaiValue'], item['khaiGrade'], item['so2Grade'], 
                    item['coGrade'], item['o3Grade'], item['no2Grade'], item['pm10Grade'], item['pm25Grade'])
        except:
            exutil.PrintException()

    def onDbConnected(self, status):        
        pass

    def onDbDisconnected(self, status):
        logging.error(status)
        time.sleep(3)
        if status == 'mysql':
            DbHelper().initMysqlWithDefault(self)
            DbHelper().initSqlAlchemyWithDefault(self)
        pass
    
    def onDbError(self, status):  #db manager
        logging.error(status)
        #if status == 'mysql':        
        #    DbHelper().restartMySql(self)
        #    DbHelper().restartSqlAlchemy(self)
        pass

    def holdInstanceUsingThread(self): 
        while self.threading:
            time.sleep(5)           
    '''
    {
      "_returnType": "json",
      "coGrade": "1",
      "coValue": "0.6",
      "dataTerm": "",
      "dataTime": "2020-03-17 21:00",
      "khaiGrade": "2",
      "khaiValue": "82",
      "mangName": "도시대기",
      "no2Grade": "2",
      "no2Value": "0.034",
      "numOfRows": "10",
      "o3Grade": "2",
      "o3Value": "0.034",
      "pageNo": "1",
      "pm10Grade": "2",
      "pm10Grade1h": "2",
      "pm10Value": "60",
      "pm10Value24": "62",
      "pm25Grade": "2",
      "pm25Grade1h": "2",
      "pm25Value": "30",
      "pm25Value24": "24",
      "resultCode": "",
      "resultMsg": "",
      "rnum": 0,
      "serviceKey": "",
      "sidoName": "",
      "so2Grade": "1",
      "so2Value": "0.003",
      "stationCode": "",
      "stationName": "단대동",
      "totalCount": "",
      "ver": ""
      '''