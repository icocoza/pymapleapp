
from datetime import datetime, timedelta
import logging 
from repository.db.InferenceMetaRepository import InferenceMetaRepository

class MetaManager:
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
        self.inferenceMetaRepository = InferenceMetaRepository()
        self.metaMap = {}   #메타정보를 캐싱함
        self.metaCreatedAtMap = {}  #캐싱된 메타정보 업데이트 위해 추가된 시간 값 저장 함
        self.deleteCheckPointAt = datetime.now()
        pass

    def getMeta(self, scode, sensorId, units):
        try:
            self._deleteNoneValue()
            key = f'{scode}-{sensorId}-{units}'
            metas = self.getMetaFromMap(key)
            if metas is not None:
                if len(metas) < 1:
                    return self._getScodeMeta(scode, units)
                return metas
            
            metas = self.inferenceMetaRepository.selectMeta(scode, sensorId, units)
            if len(metas) > 0:                
                self.metaMap[key] = metas
                self.metaCreatedAtMap[key] = datetime.now()
                return metas
            self.metaMap[key] = []
            return self._getScodeMeta(scode, units)
        except Exception as ex:
            logging.error(str(ex))
        return None

    def _getScodeMeta(self, scode, units):
        key = f'{scode}-{scode}-{units}'
        metas = self.getMetaFromMap(key)
        if metas is not None:
            return metas
        
        metas = self.inferenceMetaRepository.selectMeta(scode, scode, units)
        if len(metas) > 0:
            self.metaMap[key] = metas
            self.metaCreatedAtMap[key] = datetime.now()
            return metas
        self.metaMap[key] = []
        return None


    def getMetaFromMap(self, key):
        if key in self.metaCreatedAtMap:
            if self.metaCreatedAtMap[key] < datetime.now() - timedelta(minutes=10):
                del self.metaCreatedAtMap[key]
                del self.metaMap[key]
        if key in self.metaMap:
            return self.metaMap[key]
        return None

    
    def _deleteNoneValue(self): #for cache
        if self.deleteCheckPointAt > datetime.now() - timedelta(minutes=10):
            return

        self.deleteCheckPointAt = datetime.now()
        delete = [] 
        for key, val in self.metaMap.items(): 
            if val == None: 
                delete.append(key) 
          
        for key in delete: 
            del self.deleteCheckPointAtmetaMap[key]   
