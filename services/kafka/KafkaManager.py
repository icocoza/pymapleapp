
from module.kafka.KafkaConsumer import KafkaConsumer

class KafkaManager:
    def __init__(self, bootstrapServers, topics, groupId, consumerListener):
        self.bootstrapServers = bootstrapServers
        self.topics = topics
        self.groupId = groupId        
        self.consumerListener = consumerListener

        self.kafkaConsumers = []

    def start(self):
        topics = self.topics.split(',', -1)
        self.consumer = KafkaConsumer(self.bootstrapServers, topics, self.groupId, self.consumerListener)
        self.consumer.start()
        pass        

    def stop(self):
        self.consumer.stop()
        pass