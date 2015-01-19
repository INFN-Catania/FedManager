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

class iConsumer(metaclass=ABCMeta):
    def __init__(self,messageScheduler,configuration):
        self._ms=messageScheduler
        self._conf=configuration
        self.configure()
    @abstractmethod
    def configure(self):
        pass

class iFedMessage(metaclass=ABCMeta):
    @abstractmethod
    def setSource(self,source):
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
    def createMessageFromString(cls,msg):
        raise NotImplementedError()

class iProducer(metaclass=ABCMeta):
    def __init__(self,configuration):
        #self._ms=messageScheduler
        self._conf=configuration
        self.configure()
    @abstractmethod
    def configure(self):
        pass
    @abstractmethod
    def sendMessage(self,fedMessage):
        pass