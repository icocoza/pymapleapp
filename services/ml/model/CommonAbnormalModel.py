
import os 
import math
from keras.layers import LSTM, Dense
from keras.models import Sequential, Model, load_model
import numpy as np
from services.ml.model.LstmModel import LstmModel

from module.ml.ModelFileManager import ModelFileManager
from common.const.ModelResultType import ModelResultType
import logging

class CommonAbnormalModel(LstmModel):

    def __init__(self, sensorId, meta):

        self.sensorId = sensorId
        self.units = meta['units']
        self.lookBack = meta['lookBack']
        self.freqMin = meta['freqMin']
        self.scaleMin = meta['scaleMin']
        self.scaleMax = meta['scaleMax']
        self.outline = None
        if 'outline' in meta:
            self.outline = meta['outline']
        self.modelFile = meta['modelFile']
        pass

    def doPredict(self, endAt):
        predictionResult = self.doPredictData(self.sensorId, self.units, endAt, self.lookBack, self.freqMin, self.scaleMin, self.scaleMax)
        
        #logging.info(f'[Abnormal] Prediction: {predictionResult}')
        if predictionResult==None or math.isnan(predictionResult):
            return None
        
        score = abs(predictionResult-self.getLastValue())/self.getLastValue()*100
        score = float("{0:.3f}".format(score))
        logging.info(f'[CommonAbnormal] Prediction: {predictionResult}, Measurement Value: {self.getLastValue()} --> Score: {score}')
        if math.isnan(score) or score > 99:
            score = 100
        return (predictionResult, score)

    def getModel(self):
        return ModelFileManager.instance().getModelFromResources(self.modelFile)
 
    def getModelType(self):
        return ModelResultType.AbnormalDetection

    def postDataPreprocessor(self, df, units):
        df['value'] = df['value'].apply(self.outlier, outline=self.outline)
        return df

