import abc
class DbConnectionListener(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def onDbConnected(self, dbName):
        return

    @abc.abstractmethod
    def onDbDisconnected(self, dbName):
        return False

    @abc.abstractmethod
    def onDbError(self, dbName):
        return False