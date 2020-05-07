import abc
class KafkaConsumerListener(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def onConsumerData(self, topic, message):
        return

    @abc.abstractmethod
    def onConsumerError(self, error):
        """Called when server errors are encountered. Return False to close the stream.
        :rtype: bool
        :param error: The error object.
        :return: If True, keep listening. If False, stop the data feed.
        """
        return False