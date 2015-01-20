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

class iActor():
    __metaclass__ = ABCMeta
    """An Abstract class in which are pointed out the methods each actor must implement"""
    def __init__(self, messageScheduler, name, configuration):
        self._ms = messageScheduler
        self._configuration = configuration
        self._name = name
    """Method invoked by messaging system to delivery message to Actor
    message is a python object"""
    @abstractmethod
    def submitMessage(self, message):
        pass


