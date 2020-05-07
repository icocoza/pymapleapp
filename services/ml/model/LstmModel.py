
import os, math
from datetime import datetime
from datetime import timedelta

import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
from services.ml.model.Model import Model
import common.utils.ExceptionUtil as exutil
import logging

import abc
class LstmModel(Model):
    __metaclass__ = abc.ABCMeta

    #for Common Inference Mdoels
    timeIndexName = 'tm' #from Query in getSelectQuery()
    DEFAULT_SCALE_VALUE = 500
    def doPredictData(self, sensorId, units, endAt, lookBack, freqMin, scaleMin, scaleMax):
        try:
            dfData = self.getSampleDataForPredict(sensorId, units, endAt, lookBack, freqMin, self.timeIndexName)
            #print(dfData)
            #logging.info(f'[LstmModel] SensorId: {sensorId}, dfData: {dfData}')
            dfData = self.postDataPreprocessor(dfData, units)
            models = self.getModel()
            if models == None:
                return None
            samples = self.inputScaling(dfData, lookBack)    
            predict = models.predict(samples)
            return self.outputScaling(predict)
        except Exception as ex:
            exutil.PrintException()
            return None

    def getFreatureList(self):
        return ['value']    #from Query in getSelectQuery()

    def inputScaling(self, df, lookBack):
        # scale = scaler.fit(df[['value']])
        # # 차원 변경 계산
        # minvalue = np.ravel(scale.data_min_, order='C')
        # maxvalue = np.ravel(scale.data_max_, order='C')
        # scale_x = (df['value'].values - minvalue) / (maxvalue - minvalue)
        # scaled = pd.DataFrame(scale_x, columns=['value'])
        # scaled = scaled.interpolate()

        # return np.array(scaled['value']).reshape((1,lookBack,1))
        df['value'] = df['value'].div(self.DEFAULT_SCALE_VALUE)
        df = df.interpolate()
        return np.array(df['value']).reshape((1,lookBack,1))

    def outputScaling(self, predict):
        # minvalue = np.ravel(scaleMin, order='C')
        # maxvalue = np.ravel(scaleMax, order='C')
        # nddata = np.ravel(predict, order='c')
        # inverse_x = (nddata * (maxvalue - minvalue)) + minvalue
        
        # return np.reshape(inverse_x, (inverse_x.shape[0], 1))
        return float("{0:.3f}".format(predict[0][0] * self.DEFAULT_SCALE_VALUE))


    def getSelectQuery(self, sensorId, units, endAt, lookBack, freqMin):
        ago = lookBack * freqMin #분단위 시작값 계산
        startAt = endAt - timedelta(minutes=ago)

        startHourAt = startAt.strftime("%Y-%m-%d %H:00:00") #시간단위 시작값
        endHourAt = endAt.strftime("%Y-%m-%d %H:00:00") #시간단위 끝값

        startAt = startAt.strftime("%Y-%m-%d %H:%M:00")
        endAt = endAt.strftime("%Y-%m-%d %H:%M:00")

        query = f"SELECT tm, value \
                FROM (SELECT CONCAT(DATE_FORMAT(baseDateHour,'%%Y-%%m-%%d %%H:'),LPAD(min, 2, 0),':00') as tm, \
                ROUND(raw, 2) as value \
                FROM (SELECT sensorId, baseDateHour, \
                SUBSTRING_INDEX(SUBSTRING_INDEX(minutes, '|', n.digit+1), '|', -1) min,\
                SUBSTRING_INDEX(SUBSTRING_INDEX(raws, '|', n.digit+1), '|', -1) raw \
                FROM \
                (SELECT sensorId, baseDateHour, minutes, raws \
                FROM rbinsight_iot.iot_raws \
                WHERE baseDateHour >= '{startHourAt}' AND baseDateHour <= '{endHourAt}' AND sensorId='{sensorId}' AND units='{units}') tt1 \
                INNER JOIN \
                (SELECT 0 digit UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 \
                UNION ALL SELECT 11 digit UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19 UNION ALL SELECT 20 \
                UNION ALL SELECT 21 digit UNION ALL SELECT 22 UNION ALL SELECT 23 UNION ALL SELECT 24 UNION ALL SELECT 25 UNION ALL SELECT 26 UNION ALL SELECT 27 UNION ALL SELECT 28 UNION ALL SELECT 29 UNION ALL SELECT 30 \
                UNION ALL SELECT 31 digit UNION ALL SELECT 32 UNION ALL SELECT 33 UNION ALL SELECT 34 UNION ALL SELECT 35 UNION ALL SELECT 36 UNION ALL SELECT 37 UNION ALL SELECT 38 UNION ALL SELECT 39 UNION ALL SELECT 40 \
                UNION ALL SELECT 41 digit UNION ALL SELECT 42 UNION ALL SELECT 43 UNION ALL SELECT 44 UNION ALL SELECT 45 UNION ALL SELECT 46 UNION ALL SELECT 47 UNION ALL SELECT 48 UNION ALL SELECT 49 UNION ALL SELECT 50 \
                UNION ALL SELECT 51 digit UNION ALL SELECT 52 UNION ALL SELECT 53 UNION ALL SELECT 54 UNION ALL SELECT 55 UNION ALL SELECT 56 UNION ALL SELECT 57 UNION ALL SELECT 58 UNION ALL SELECT 59 UNION ALL SELECT 60 ) n \
                ON LENGTH(REPLACE(minutes, '|' , '')) <= LENGTH(minutes)-n.digit) tt2) tt3 \
                WHERE tm >= '{startAt}' AND tm <= '{endAt}'"
        #print(query)
        return query