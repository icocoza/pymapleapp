import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from module.db.SqlAlchemyMgr import SqlAlchemyMgr
import logging
import abc
class Model:

    __metaclass__ = abc.ABCMeta
    DEFAULT_OUTLINE_VALUE = 500

    @abc.abstractmethod
    def doPredict(self):
        return

    @abc.abstractmethod
    def getModel(self):
        return

    @abc.abstractmethod
    def getModelType(self):
        return

    def getLastValue(self):
        if self._lastValue == 0:
            self._lastValue = 0.01 #score 계산시 0으로 나뉘지 않도록 0.01(0에 가까운 값)을 셋팅하도록 함
        return self._lastValue

    @abc.abstractmethod
    def inputScaling(self, df, lookBack):
        return

    @abc.abstractmethod
    def outputScaling(self, predict):
        return

    @abc.abstractmethod
    def getSelectQuery(self, sensorId, units, endAt, lookBack, freqMin):
        return

    @abc.abstractmethod
    def getFreatureList(self):
        return

    @abc.abstractmethod
    def postDataPreprocessor(self, df, units):
        return

    def getSampleDataForPredict(self, sensorId, units, endAt, lookBack, freqMin, timeIndexName):
        df = self._getDataFrame(sensorId, units, endAt, lookBack, freqMin)
        if df.empty:
            return None
        df.iloc[:, 1:] = df.iloc[:, 1:].astype('float64')
        self._lastValue = df.iloc[len(df)-1, 1]

        startAt = datetime.strptime(self._calcStartAtTime(endAt, lookBack, freqMin).strftime("%Y-%m-%d %H:%M:00"), "%Y-%m-%d %H:%M:00")
        dfDummy = self._getDummyDataFrame(startAt, lookBack, str(freqMin) + 'T', timeIndexName, self.getFreatureList())

        if freqMin == 1:    #1분 보다 큰 freqMin일 경우에는 freqMin 값으로 round처리하여 시간 자리수를 맞춰야 함
            df = df.set_index(timeIndexName)
            df.index = pd.to_datetime(df.index)
        else:
            df = self._normalizeDataFrameFrequencyMinutes(df, timeIndexName, freqMin)     
            dfDummy = self._normalizeDataFrameFrequencyMinutes(dfDummy, timeIndexName, freqMin)
        dfDummy.update(df)
        dfData = dfDummy
        #print(dfData)
        for x in range(len(dfData.columns)):
            if pd.isna(dfData.iloc[0, x]):
                dfData.iloc[0, x] = 0
        return dfData

    def outlier(self, data, outline=DEFAULT_OUTLINE_VALUE):
        if outline == None:
            outline = self.DEFAULT_OUTLINE_VALUE
        if data >= outline:
            return np.nan
        return data


    def _getDataFrame(self, sensorId, units, endAt, lookBack, freqMin):
        query = self.getSelectQuery(sensorId, units, endAt, lookBack, freqMin)
        return SqlAlchemyMgr.instance().select(query)

    def _getDummyDataFrame(self, startAt, lookBack, freq, indexName, features):
        dfDummy = pd.date_range(startAt, periods=lookBack, freq=freq, name=indexName)
        dfDummy = dfDummy.to_frame(index=True)
        dfDummy.reset_index(drop=True, inplace=True)
        for feature in features:
            dfDummy[feature] = np.NaN
        dfDummy = dfDummy.set_index(indexName)
        return dfDummy

    def _normalizeDataFrameFrequencyMinutes(self, df, timeIndexName, freqMin): #usually timeIndexName is 'tm'
        if df.index.name == timeIndexName:
            df = df.reset_index()
        df[timeIndexName] = pd.to_datetime(df[timeIndexName])
        df[timeIndexName] = df[timeIndexName].dt.round(str(freqMin) + 'min')
        df = df.set_index(timeIndexName)
        return df.reset_index().drop_duplicates(subset=timeIndexName, keep='first').set_index(timeIndexName)

    def _calcStartAtTime(self, endAt, lookBack, freqMin):
        ago = lookBack * freqMin        #분단위 시작값 계산
        startAt = endAt - timedelta(minutes=ago)
        return startAt