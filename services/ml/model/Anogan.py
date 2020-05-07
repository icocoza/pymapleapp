import ml.anogan.anogan_batch as anogan
import datetime
from db.mlDbhelper import MlDbHelper
import appconfig
from utils.eventhook import EventHook
import logging
import pandas as pd
import numpy as np

class Anogan:
    def __init__(self):
        self.onEventDbError = EventHook()
        self.onEventDbError += self.on_error
        self.onEventDbDisconnect = EventHook()
        self.onEventDbDisconnect += self.on_disconnected
        self.mlDb = MlDbHelper()
        self.mlDb.init(appconfig.DB_HOST, appconfig.DB_PORT, appconfig.DB_USER, appconfig.DB_PASSWORD, appconfig.DB_NAME, self)

    def doAnalysisPM2_5(self, scode, sensorId, units):
        self._doAnalysisDust(scode, sensorId, units, 'pm2.5')
        pass

    def doAnalysisPM10(self, scode, sensorId, units):
        self._doAnalysisDust(scode, sensorId, units, 'pm10')
        pass

    def _doAnalysisDust(self, scode, sensorId, units, sensorType):
        df24h = self._load_data_24h(scode, sensorId, units)
        dataX = np.array(df24h) #DF to array
        dataY = dataX[-1]       #set last X data to Y
        anomaly_score, y_pred = anogan.compute_anomaly_score(dataX, sensor_type = sensorType)
        '''
        anomaly_scores, gen_x = mutiple_anomaly_score(dataX, sensor_type= sensor_type_)
        anomaly_scores = np.array(anomaly_scores).reshape(-1, 1)
        anomaly_scores = np.concatenate((sensors, anomaly_scores), axis=1)
        gen_x = np.vstack(gen_x)
        gen_x = np.concatenate((sensors, gen_x), axis=1)
        print("score : ", anomaly_scores, " y_pred : ",gen_x)
        '''
        print(anomaly_score)
        print(y_pred)
        pass

    def _load_data_24h(self, scode, sensorId, units):
        end = datetime.datetime.now()
        endDateHour = end.strftime('%Y-%m-%d %H:00')
        start = end - datetime.timedelta(hours=self.LOOKBACK)
        startDateHour = start.strftime('%Y-%m-%d %H:00')
        hourlyDf = self._makeEmptyHourlyDataFrame(start, self.LOOKBACK) #lookback 시간동안의 빈 DF를 먼저 생성함
        try:
            dfStat = self.mlDb.select24HourMeanStat(scode, sensorId, startDateHour, endDateHour, units)            
            df = dfStat.set_index('baseDateHour')
            df.index = pd.to_datetime(df.index)
            df.columns = ['value']
            hourlyDf.update(df) #빈 DF에 값이 있는 DF를 업데이트하여 정확한 lookback 카운트를 맞춤(why? 센서값은 빈 시간값이 존재할 수 있기에)
            logging.info(hourlyDf)
            return hourlyDf
        except Exception as e:
            logging.error(str(e))

    def on_error(self, error):
        pass

    def on_disconnected(self, error):
        pass

    def _makeEmptyHourlyDataFrame(self, start, lookbackHours):
        start = start + datetime.timedelta(hours=1)
        startDateHour = start.strftime('%Y-%m-%d %H:00')
        dfDateRange = pd.date_range(startDateHour, periods=lookbackHours, freq='H', name='date')    # 날짜 인덱스만 가진 DataFrame 생성
        df = dfDateRange.to_frame(index=True)    # 일반 DataFrame로 변경
        df.reset_index(drop=True, inplace=True) # DateTimeIndex를 일반 Column으로 변경
        df["value"] = pd.np.nan # value column을 추가하고 Nan으로 할당
        return df.set_index('date') #date column을 인덱스로 지정