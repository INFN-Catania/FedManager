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
from fednodes.abstract_classes import iFedMessage, iConsumer, iProducer
import threading
import posix_ipc
import json


def _simpleMessageDeserializer(msgstring):
        msgarr = msgstring.split("|")
        return DummyFedMessage(msgarr[0], json.loads(msgarr[1]),msgarr[2],msgarr[3])


class DummyFedMessage(iFedMessage):
    def __init__(self,target,body,bodyUriType,source=None):
        self._target = target
        self._source = source
        self._body = body
        self._bodyUriType = bodyUriType
    def setSource(self,source):
        self._source = source
    def getSource(self):
        return self._source
    def getTarget(self):
        return self._target
    def getBody(self):
        return self._body
    def getBodyUriType(self):
        return self._bodyUriType
    def toString(self):
        return self.getTarget() + "|" + json.dumps(self.getBody()) +"|" + self.getBodyUriType() + "|" + self.getSource()
    @classmethod
    def createMessageFromString(cls,msg):
        msgarr = msg.split("|")
        return DummyFedMessage(msgarr[0], json.loads(msgarr[1]),msgarr[2],msgarr[3])


class DummyPosixIPCConsumer(iConsumer,threading.Thread):
    def __init__(self,messageScheduler,configuration):
        threading.Thread.__init__(self)
        super(DummyPosixIPCConsumer,self).__init__(messageScheduler,configuration)
    def configure(self):
        queue = "/" + self._conf["mom.consumer.topic"]
        self._running = True
        try:
            posix_ipc.unlink_message_queue(queue)
        except posix_ipc.ExistentialError:
            pass
        print("Apro queue: " + queue)
        self._mq = posix_ipc.MessageQueue(queue, posix_ipc.O_CREAT)
        self.start()

    def run(self):
        while self._running:
            msg, _ = self._mq.receive()
            msg = msg.decode()
            message = DummyFedMessage.createMessageFromString(msg)
            #print(__name__ + " Arrivato messaggio con corpo : " + message.getBody())
            self._ms.serveMessage(message)


    def end(self):
        self._running = False

class DummyPosixIPCProducer(iProducer):
    def configure(self):
        pass
    def sendMessage(self,fedMessage):
        target = "/"+fedMessage.getTarget()
        mq = posix_ipc.MessageQueue(target)
        mq.send(fedMessage.toString())
        mq.close()
