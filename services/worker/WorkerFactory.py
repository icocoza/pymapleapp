
from services.worker.MapleWorker import MapleWorker

class WorkerFactory:

    workerMap = {}
    def createFactory(self, stype):
        #print(meta)
        if stype in self.workerMap:
            return self.workerMap[stype]

        if stype == 'maple':
            worker = MapleWorker()
            self.workerMap[stype] = worker
            return worker
        else:
            return None