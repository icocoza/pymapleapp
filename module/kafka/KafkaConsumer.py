from threading import Thread
from time import sleep
import logging
import json

from confluent_kafka import Consumer, KafkaError, TopicPartition
import IotDataProcessor
#from inspect import getsourcefile
#import os.path as path, sys
#current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
#sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from common.inf.ConsumerListener import ConsumerListener

class KafkaConsumer(Thread):
    def __init__(self, bootstrapServers, topics, groupId, consumerListener):
        Thread.__init__(self)
        self.running = True
        self.bootstrapServers = bootstrapServers
        self.topics = topics
        self.groupId = groupId        
        self.consumerListener = consumerListener
        pass

    def run(self):        
        self.consumer = Consumer({'bootstrap.servers': self.bootstrapServers,
                      'group.id': self.groupId,
                      'enable.auto.commit': True,
                      'on_commit': self.onCommit,
                      'default.topic.config': {'auto.offset.reset': 'latest'}})
        
        self.consumer.subscribe(self.topics)
        while self.running:
            msg = self.consumer.poll(1.0)

            if msg is None:
                sleep(3)
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            #print('Topic: {}, Received message: {}'.format(msg.topic(), msg.value().decode('utf-8')))
            self.consumerListener.onConsumerData(msg.topic(), msg.value().decode('utf-8'))
        self.consumer.close()
        pass
    
    def stop(self):
        self.running = False

    def onCommit(self, err, partitions):
        #print(partitions)
        #tp = TopicPartition(self.topics)
        #logging.info(self.consumer.assignment(tp))
        pass
