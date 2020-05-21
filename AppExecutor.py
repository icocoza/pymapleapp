from AppPreprocessor import AppPreprocessor
from services.scheduler.AirKoreaCollector import AirKoreaCollector

class AppExecutor:
    
    def start(self, serviceType, buildType):
        self.app = self._executor(serviceType, buildType)
        if self.app != None:
            self.app.start()
            return True
        return False

    def stop(self):
        if self.app != None:
            self.app.stop()
        pass

    def _executor(self, serviceType, buildType):
        print('Type: ', str(serviceType))
        if serviceType == 'maple':
            return AppPreprocessor(serviceType, buildType)
        return None
