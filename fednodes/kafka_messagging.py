"""
  Copyright 2015 INFN (Italy)

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
"""
__author__ = 'maurizio'
from fednodes.abstract_classes import iConsumer, iProducer
from kafka import KafkaClient, MultiProcessConsumer, SimpleConsumer, SimpleProducer
import threading


class KafkaConsumer(iConsumer,threading.Thread):
    def __init__(self,messageScheduler,configuration):
        threading.Thread.__init__(self)
        super(KafkaConsumer,self).__init__(messageScheduler,configuration)

    def configure(self):
        topic = self._conf["mom.consumer.topic"]
        brokerlist = self._conf["mom.producer.brokerlist"]
        try:
            numprocs= self._conf["mom.consumer.numthread"]
        except:
            numprocs = 4
        self._kafka = KafkaClient(brokerlist)
        #self._consumer = MultiProcessConsumer(self._kafka, "aaa", topic, num_procs=float(numprocs))
        self._consumer = SimpleConsumer(self._kafka, "aaa", topic)
        self.start()

    def run(self):
        for message in self._consumer:
            msg=message.message.value.decode('utf-8')
            self._ms.serveMessage(msg)


    def end(self):
        self._running = False

class KafkaProducer(iProducer):
    def configure(self):
        brokerlist = self._conf["mom.producer.brokerlist"]
        self._kafka = KafkaClient(brokerlist)
        self._producer = SimpleProducer(self._kafka, async=False,
                          req_acks=SimpleProducer.ACK_AFTER_LOCAL_WRITE,
                          ack_timeout=2000)
    def sendMessage(self,fedMessage,topic):
        response = self._producer.send_messages(topic, fedMessage)
        if response:
            """check error"""
            #print(response[0].error)
            #print(response[0].offset)

