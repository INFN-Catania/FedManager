import unittest

import time
__author__ = 'maurizio'
from fednodes.dummy_classes import DummyPosixIPCConsumer, DummyPosixIPCProducer, DummyFedMessage
from fednodes.messaging import MessageScheduler
from fednodes.kafka_messagging import KafkaConsumer,KafkaProducer
from fednodes.abstract_classes import Fednode
from actors.dummy_actors import ActorTest
from actors.federator import FederationManager

class testFedNode(unittest.TestCase):
    _conf = {}
    def setUp(self, _conf=None):
        self._configuration = { "mom.consumer.topic": "federation_site",
                                "test.targetMessage" : "federation_site",
                                "mom.producer.brokerlist" : "193.206.209.83:9092",
                                "mom.consumer.numthread" : "2"}


    def Atest_fednode(self):
        sitefed = Fednode(self._configuration,
                          DummyFedMessage,
                          DummyPosixIPCConsumer,
                          DummyPosixIPCProducer,
                          )

        Afedman = FederationManager(sitefed.get_ms(),
                                    sitefed.get_configuration())

        site1 = Fednode({"mom.consumer.topic": "site1",
                         "test.targetMessage" : "federation_site",
                         "mom.producer.brokerlist" : "localhost:9092",
                         "mom.consumer.numthread" : "2"},
                          DummyFedMessage,
                          DummyPosixIPCConsumer,
                          DummyPosixIPCProducer,
                        )



        testA = ActorTest(site1.get_ms(),
                          "fedManager_site_1",
                          site1.get_configuration(),
                          "ToSiteFedManager",
                          "ToFederationManager")
        site2 = Fednode({
                            "mom.consumer.topic": "site2",
                            "test.targetMessage" : "federation_site",
                            "mom.producer.brokerlist" : "localhost:9092",
                            "mom.consumer.numthread" : "2"
                        },
                        DummyFedMessage,
                        DummyPosixIPCConsumer,
                        DummyPosixIPCProducer,
                       )



        testA = ActorTest(site2.get_ms(),
                          "fedManager_site_2",
                          site2.get_configuration(),
                          "ToSiteFedManager",
                          "ToFederationManager")



    def test_KafkaActorMessagingfednode(self):
        sitefed = Fednode(self._configuration,
                          DummyFedMessage,
                          KafkaConsumer,
                          KafkaProducer,
                          )

        Afedman = FederationManager(sitefed.get_ms(),
                                    sitefed.get_configuration())

        site1 = Fednode({       "mom.consumer.topic": "site1",
                                "test.targetMessage" : "federation_site",
                                "mom.producer.brokerlist" : "193.206.209.83:9092",
                                "mom.consumer.numthread" : "2"},
                          DummyFedMessage,
                          KafkaConsumer,
                          KafkaProducer,
                          )


        testA = ActorTest(site1.get_ms(),
                          "testA",
                          site1.get_configuration(),
                          "ToSiteFedManager",
                          "ToFederationManager")



    def Atest_fed(self):
        Afedman = FederationManager(self._ms, self._configuration)
        conf=self._configuration
        conf["mom.consumer.topic"]= "site2"
        testA = ActorTest(self._ms,
                          "testA",
                          conf,
                          "ToSiteFedManager",
                          "ToFederationManager")
        #self._configuration["mom.consumer.topic"]= "site2"

        #testB = ActorTest(self._ms, "testB", self._configuration, "ToSiteFedManager", "ToFederationManager")

    def Atest_KafkaActorMessaging(self):
        self._producer = KafkaProducer(self._configuration)
        self._ms = MessageScheduler(DummyFedMessage,self._producer, self._configuration)
        self._consumer = KafkaConsumer( self._ms, self._configuration)
        Afedman = FederationManager(self._ms, self._configuration)
        testA = ActorTest(self._ms, "testA", self._configuration, "ToSiteFedManager", "ToFederationManager")
        #testA = ActorTest(self._ms, "testA", self._configuration, "http://onto/type1", "http://onto/type2")
        #testB = ActorTest(self._ms, "testB", self._configuration, "http://onto/type2", "http://onto/type1")
        #testC = ActorTest(self._ms, "testC", self._configuration, "http://onto/type1", "http://onto/type2")



if __name__ == '__main__':
    unittest.main()