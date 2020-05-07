
import os 
from keras.layers import LSTM, Dense
from keras.models import Sequential, Model, load_model

class ModelFileManager:
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
        self.sensorModelMap = {}
        self.modelFilesMap = {}
        pass

    def getModelFromResources(self, modelFile):
        if modelFile in self.modelFilesMap:
            return self.modelFilesMap[modelFile]        
        modelPath = os.getcwd() + "/resources/weight/" + modelFile 
        if os.path.exists(modelPath) == False:
            return None

        model = load_model(modelPath)
        self.modelFilesMap[modelFile] = model
        return model

    def getModelFromPath(self, modelFile):
        if modelFile in self.modelFilesMap:
            return self.modelFilesMap[modelFile]
        if os.path.exists(modelFile) == False:
            return None

        model = load_model(modelFile)
        self.modelFilesMap[modelFile] = model
        return model

    
 
