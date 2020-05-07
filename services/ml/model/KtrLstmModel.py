
import os, math
import logging
from keras.layers import LSTM, Dense
from keras.models import Sequential, Model, load_model
import numpy as np
from services.ml.model.LstmModel import LstmModel

from module.ml.ModelFileManager import ModelFileManager
from common.const.ModelResultType import ModelResultType

class KtrLstmModel(LstmModel): #박진영M PM10모델

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
        modifiedFreqMin = 5 # lookback 을 5분 단위로 계산해 달라함 by Jinyoung Park
        predictionResult = self.doPredictData(self.sensorId, self.units, endAt, self.lookBack, modifiedFreqMin, self.scaleMin, self.scaleMax)
        if predictionResult == None or math.isnan(predictionResult):
            logging.info(f'[LSTM] sensorId: {self.sensorId} Prediction Failed')
            return None
        logging.info(f'[LSTM] sensorId: {self.sensorId}, Prediction: {predictionResult}, Measurement Value: {self.getLastValue()}')
        return predictionResult

    def getModel(self):
        logging.info(f'sensorId: {self.sensorId}, modelFile: {self.modelFile}')
        return ModelFileManager.instance().getModelFromResources(self.modelFile)
 
    def getModelType(self):
        return ModelResultType.Pediction

    def getModelName(self):
        return self.modelName

    def postDataPreprocessor(self, df, units):
        df = df.resample('5T').first()
        df['value'] = df['value'].apply(self.outlier, outline=self.outline)
        return df

    def inputScaling(self, df, lookBack):
        df['value'] = df['value'].div(self.scaleMax)
        df = df.interpolate()
        return np.array(df['value']).reshape((1,lookBack,1))

    def outputScaling(self, predict):
        return float("{0:.3f}".format(predict[0][0] * self.scaleMax))
