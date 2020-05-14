
import abc

class Action:
    
    def setError(self, scode, msg):
        return {'scode': scode, 'result': 'error', 'data': msg}

    def setOk(self, scode, msg):
        return {'scode': scode, 'result': 'ok', 'data': msg}

    def _getShortContent(self, content):
        if len(content) < 55:
            return content
        return content[:54] + "...(More)"
