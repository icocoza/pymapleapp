import abc
class DbConnectionListener(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def onDbConnected(self, status):
        return

    @abc.abstractmethod
    def onDbDisconnected(self, error):
        return False

    @abc.abstractmethod
    def onDbError(self, error):
        return False