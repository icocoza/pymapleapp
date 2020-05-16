from AppProcessor import AppProcessor
from services.scheduler.AirKoreaCollector import AirKoreaCollector

class AppExecutor:
    
    def start(self, type):
        self.app = self._executor(type)
        if self.app != None:
            self.app.start()
            return True
        return False

    def stop(self):
        if self.app != None:
            self.app.stop()
        pass

    def _executor(self, type):
        print('Type: ', str(type))
        if type == 'maple':
            return AppProcessor()
        return None
