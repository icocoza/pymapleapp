
from services.worker.MapleWorker import MapleWorker

class WorkerFactory:

    workerMap = {}
    def createFactory(self, scode):
        #print(meta)
        if scode in workerMap:
            return workerMap[scode]

        if scode == 'maple':
            worker = MapleWorker()
            workerMap[scode] = worker
            return worker
        else:
            return None