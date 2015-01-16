import unittest

import time
__author__ = 'maurizio'
from fednodes.dummy_classes import DummyPosixIPCConsumer, DummyPosixIPCProducer, DummyFedMessage
from fednodes.messaging import MessageScheduler
from actors.dummy_actors import ActorTest


class testFedNode(unittest.TestCase):
    _conf = {}
    def setUp(self, _conf=None):
        self._configuration = { "mom.consumer.topic": "test", "test.targetMessage" : "test" }
        self._producer = DummyPosixIPCProducer(self._configuration)
        self._ms = MessageScheduler(self._producer, self._configuration)
        self._consumer = DummyPosixIPCConsumer( self._ms, self._configuration)




    def Atest_dummyipc(self):
        producer = DummyPosixIPCProducer(self._conf)
        message = DummyFedMessage("test","il corpo del messaggio","il tipo di messaggio")
        consumer = DummyPosixIPCConsumer("lo scheduler", self._configuration)
        print("consumer created")
        for x in range(5):
            producer.sendMessage(message)

    def test_ActorMessaging(self):
        testA = ActorTest(self._ms, "testA", self._configuration, "http://onto/type1", "http://onto/type2")
        testB = ActorTest(self._ms, "testB", self._configuration, "http://onto/type2", "http://onto/type1")
        testB = ActorTest(self._ms, "testC", self._configuration, "http://onto/type1", "http://onto/type2")


if __name__ == '__main__':
    unittest.main()