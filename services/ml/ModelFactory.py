

from services.ml.model.CommonLstmModel import CommonLstmModel
from services.ml.model.CommonAbnormalModel import CommonAbnormalModel
from services.ml.model.Dos200AbnormalModel import Dos200AbnormalModel
from services.ml.model.KtrLstmModel import KtrLstmModel
class ModelFactory:

    #Case를 좀더 수집해서 향후에 깔끔하게 정리합시다
    def createFactory(self, sensorId, meta):
        #print(meta)
        if meta['models'] == 'CommonLstmModel':
            return CommonLstmModel(sensorId, meta)
        elif meta['models'] == 'CommonAbnormalModel':
            return CommonAbnormalModel(sensorId, meta)
        elif meta['models'] == 'Dos200AbnormalModel':
            return Dos200AbnormalModel(sensorId, meta)
        elif meta['models'] == 'KtrLstmModel':
            return KtrLstmModel(sensorId, meta)
        else:
            return None