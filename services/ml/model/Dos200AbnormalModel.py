
import os 
import math
from datetime import datetime
from datetime import timedelta

import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

from services.ml.model.Model import Model
from module.ml.ModelFileManager import ModelFileManager
from common.const.ModelResultType import ModelResultType
from services.ml.AirKorManager import AirKorManager
import logging
import common.utils.ExceptionUtil as exutil
import abc
class Dos200AbnormalModel(Model):
    
    #for Common Inference Mdoels
    timeIndexName = 'tm' #from Query in getSelectQuery()

    def __init__(self, sensorId, meta):
        self.sensorId = sensorId
        self.units = meta['units']
        self.lookBack = meta['lookBack']
        self.freqMin = meta['freqMin']
        self.scaleMin = meta['scaleMin']
        self.scaleMax = meta['scaleMax']

        self.modelName = meta['models']
        self.modelFile = meta['modelFile']
        self.outline = None
        if 'outline' in meta:
            self.outline = meta['outline']
        pass

    def doPredict(self, endAt):
        predictionResult = self.doPredictData(self.sensorId, self.units, endAt, self.lookBack, self.freqMin, self.scaleMin, self.scaleMax)
        if predictionResult == None or math.isnan(predictionResult):
            logging.info(f'[Dos200Abnormal] sensorId: {self.sensorId} Prediction Failed.')
            return None
        lastValue = self.getLastValue()
        airQuality = None
        if self.sensorId == '702c1ffffe548e50': #인천-용현
            #airQuality = AirKorManager.instance().getAirQualityBySensorAt('인천', '연희', endAt)
            airQuality = AirKorManager.instance().getAirQuality('인천', '연희')
        #airQuality = AirKorManager.instance().getAirQuality('인천', '연희')
        if airQuality != None:
            lastValue = float(airQuality[self._unitNoToStr(self.units)])

        lastValue = lastValue + 0.001 #for avoid divide by 0
        score = abs(predictionResult - lastValue) / lastValue * 100
        score = float("{0:.3f}".format(score))
        logging.info(f'[Dos200Abnormal] sensorId: {self.sensorId}, Prediction: {predictionResult}, Measurement Value: {self.getLastValue()} / AirKorea: {lastValue} --> Score: {score}')
        if math.isnan(score) or score > 99:
            score = 100
        return (predictionResult, score)


    def getModel(self):
        return ModelFileManager.instance().getModelFromResources(self.modelFile)
 
    def getModelType(self):
        return ModelResultType.AbnormalDetection

    def getModelName(self):
        return self.modelName
        
    def getFreatureList(self):
        return ['pm10', 'temp', 'humid']    #from Query in getSelectQuery()

    def postDataPreprocessor(self, df, units):
        return df

    def doPredictData(self, sensorId, units, endAt, lookBack, freqMin, scaleMin, scaleMax):
        try:
            dfData = self.getSampleDataForPredict(sensorId, units, endAt, lookBack, freqMin, self.timeIndexName)
            #print(dfData)
            models = self.getModel()
            if models == None:
                return None
            samples = self.inputScaling(dfData, lookBack)  
            predict = models.predict(samples)
            result = self.outputScaling(predict)
            logging.info('after: ' + str(result))
            predictinResult = float("{0:.3f}".format(result))
            return predictinResult
        except Exception as ex:
            exutil.PrintException()
            return None

    def inputScaling(self, df, lookBack):
        df['pm10'] = df['pm10'].div(self.scaleMax)
        df['temp'] = df['temp'].div(100)
        df['humid'] = df['humid'].div(100)
        df = df.interpolate()
        return np.array(df[['pm10', 'temp', 'humid']]).reshape((1,lookBack,3))

    def outputScaling(self, predict):
        return predict[0][0] * self.scaleMax

    def getSelectQuery(self, sensorId, units, endAt, lookBack, freqMin):
        ago = lookBack * freqMin #분단위 시작값 계산
        startAt = endAt - timedelta(minutes=ago)

        startHourAt = startAt.strftime("%Y-%m-%d %H:00:00") #시간단위 시작값
        endHourAt = endAt.strftime("%Y-%m-%d %H:00:00") #시간단위 끝값

        startAt = startAt.strftime("%Y-%m-%d %H:%M:00")
        endAt = endAt.strftime("%Y-%m-%d %H:%M:00")

        query = f"SELECT tm, \
                SUM(CASE WHEN units='{units}' THEN raw END) pm10, \
                SUM(CASE WHEN units='1' THEN raw END) temp, \
                SUM(CASE WHEN units='2' THEN raw END) humid \
                FROM (SELECT CONCAT(DATE_FORMAT(baseDateHour,'%%Y-%%m-%%d %%H:'),LPAD(min, 2, 0),':00') as tm, \
                ROUND(raw*0.1, 2) as raw, units \
                FROM (SELECT sensorId, baseDateHour, units, \
                SUBSTRING_INDEX(SUBSTRING_INDEX(minutes, '|', n.digit+1), '|', -1) min,\
                SUBSTRING_INDEX(SUBSTRING_INDEX(raws, '|', n.digit+1), '|', -1) raw \
                FROM \
                (SELECT sensorId, baseDateHour, units, minutes, raws \
                FROM rbinsight_iot.iot_raws \
                WHERE baseDateHour >= '{startHourAt}' AND baseDateHour <= '{endHourAt}' AND sensorId='{sensorId}') tt1 \
                INNER JOIN \
                (SELECT 0 digit UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 \
                UNION ALL SELECT 11 digit UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19 UNION ALL SELECT 20 \
                UNION ALL SELECT 21 digit UNION ALL SELECT 22 UNION ALL SELECT 23 UNION ALL SELECT 24 UNION ALL SELECT 25 UNION ALL SELECT 26 UNION ALL SELECT 27 UNION ALL SELECT 28 UNION ALL SELECT 29 UNION ALL SELECT 30 \
                UNION ALL SELECT 31 digit UNION ALL SELECT 32 UNION ALL SELECT 33 UNION ALL SELECT 34 UNION ALL SELECT 35 UNION ALL SELECT 36 UNION ALL SELECT 37 UNION ALL SELECT 38 UNION ALL SELECT 39 UNION ALL SELECT 40 \
                UNION ALL SELECT 41 digit UNION ALL SELECT 42 UNION ALL SELECT 43 UNION ALL SELECT 44 UNION ALL SELECT 45 UNION ALL SELECT 46 UNION ALL SELECT 47 UNION ALL SELECT 48 UNION ALL SELECT 49 UNION ALL SELECT 50 \
                UNION ALL SELECT 51 digit UNION ALL SELECT 52 UNION ALL SELECT 53 UNION ALL SELECT 54 UNION ALL SELECT 55 UNION ALL SELECT 56 UNION ALL SELECT 57 UNION ALL SELECT 58 UNION ALL SELECT 59 UNION ALL SELECT 60 ) n \
                ON LENGTH(REPLACE(minutes, '|' , '')) <= LENGTH(minutes)-n.digit) tt2) tt3 \
                WHERE tm >= '{startAt}' AND tm <= '{endAt}' group by tm"

        return query

    def _unitNoToStr(self, units):
        if units == '7':
            return 'pm10'
        elif units == '8':
            return 'pm25'
        return ""