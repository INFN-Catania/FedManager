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
from actors.abstract_classes import iActor
from fednodes.dummy_classes import DummyFedMessage
import threading
import time


class ActorTest(iActor,threading.Thread):
    """Actor for test"""
    def __init__(self, messageScheduler, name, configuration, typetomanage, typetarget):
        super(ActorTest,self).__init__(messageScheduler, name, configuration)
        messageScheduler.registerActor(typetomanage,self)
        self._typetarget = typetarget
        threading.Thread.__init__(self)
        self._name = name
        self._configuration = configuration
        self.start()

    def submitMessage(self, fedMessage):
        print("Test actor '" + self._name + "received a message of type: '" + fedMessage.getBodyUriType()+"'")
        print(fedMessage.getBody())

    def run(self):
        while True:
            body={"funzione": "funzione1" , "args": "arguments", "from": self._name}
            msg = DummyFedMessage(self._configuration["test.targetMessage"], body, self._typetarget)
            self._ms.sendMessage(msg)
            time.sleep(2)








