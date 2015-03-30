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
from abc import ABCMeta, abstractmethod
from fednodes.messaging import MessageScheduler


class iConsumer(object):
    __metaclass__ = ABCMeta

    def __init__(self, messageScheduler, configuration):
        self._ms = messageScheduler
        self._conf = configuration
        self.configure()

    @abstractmethod
    def configure(self):
        pass


class iProducer():
    __metaclass__ = ABCMeta

    def __init__(self, configuration):
        # self._ms=messageScheduler
        self._conf = configuration
        self.configure()

    @abstractmethod
    def configure(self):
        pass

    @abstractmethod
    def sendMessage(self, fedMessageAsString, topic_target):
        pass


# TODO: add 'add_actor'
class Fednode():
    def __init__(self, configuration, message_class, consumer_class, producer_class):
        self._configuration = configuration
        producer = producer_class(configuration)
        self._ms = MessageScheduler(message_class, producer, configuration)
        consumer = consumer_class(self._ms, configuration)

    def get_configuration(self):
        return self._configuration

    def get_ms(self):
        return self._ms


class iFedMessage():
    __metaclass__ = ABCMeta

    @abstractmethod
    def setSource(self, source):
        pass

    @abstractmethod
    def setId(self, id):
        pass

    @abstractmethod
    def getId(self):
        pass

    @abstractmethod
    def getSource(self):
        pass

    @abstractmethod
    def getTarget(self):
        pass

    @abstractmethod
    def getBody(self):
        pass

    @abstractmethod
    def getBodyUriType(self):
        pass

    @abstractmethod
    def toString(self):
        pass

    @classmethod
    def createMessageFromString(cls, msg):
        raise NotImplementedError()

