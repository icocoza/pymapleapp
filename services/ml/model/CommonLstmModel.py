
import os, math
import logging
from keras.layers import LSTM, Dense
from keras.models import Sequential, Model, load_model

from services.ml.model.LstmModel import LstmModel

from module.ml.ModelFileManager import ModelFileManager
from common.const.ModelResultType import ModelResultType

class CommonLstmModel(LstmModel):

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
        if predictionResult==None or math.isnan(predictionResult):
            return None

        logging.info(f'[LSTM] Prediction: {predictionResult}, Measurement Value: {self.getLastValue()}')
        return predictionResult

    def getModel(self):
        return ModelFileManager.instance().getModelFromResources(self.modelFile)
 
    def getModelType(self):
        return ModelResultType.Pediction

    def getModelName(self):
        return self.modelName

    def postDataPreprocessor(self, df, units):
        return df
