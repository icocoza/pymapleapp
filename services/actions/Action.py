
import abc

class Action:
    
    def setError(self, scode, msg):
        return {'scode': scode, 'result': 'error', 'data': msg}

    def setOk(self, scode, msg):
        return {'scode': scode, 'result': 'ok', 'data': msg}