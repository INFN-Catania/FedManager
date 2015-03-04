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
from actors.abstract_classes import Actor
from fednodes.dummy_classes import DummyFedMessage
import threading
import time
from actors.federation_costants import *
from datetime import datetime, timedelta

class ActorTest(Actor,threading.Thread):
    """Actor for test"""
    def __init__(self, messageScheduler, name, configuration, typetomanage, typetarget):
        super(ActorTest,self).__init__(messageScheduler, name, configuration)
        messageScheduler.registerActor(typetomanage,self)
        self._typetarget = typetarget
        threading.Thread.__init__(self)
        self._name = name
        self._configuration = configuration
        self._fedoperations = {
            OP_FEDERATOR_JOIN_FEDERATION_SUCCESS: {"handler": self._join_federation_success, OP_INIT_TRANSACTION: False},
            OP_FEDERATOR_JOIN_FEDERATION_FAIL: {"handler": self._join_federation_fail, OP_INIT_TRANSACTION: False}
        }
        self.start()

    """def submitMessage(self, fedMessage):
        print("Test actor '" + self._name + " received a message of type: '" + fedMessage.getBodyUriType()+"'")
        print(fedMessage.getBody())
    """
    def run(self):
        body={"operation": OP_SITE_JOIN_FEDERATION_REQUEST, "argument": {"request": 1}}

        messageid= self.createTransaction(state=STATE_RES_REQ_SENT, applicant="test", expiration_time=datetime.now() + timedelta(days=1), arg="prova")

        #while True:
            #body={"funzione": "funzione1" , "args": "arguments", "from": self._name}
        msg = DummyFedMessage(
                        target=self._configuration["test.targetMessage"],
                        body=body,
                        bodyUriType=self._typetarget,
                        id=messageid)
        self._ms.sendMessage(msg)
        time.sleep(2)

    def _join_federation_success(self,applicant, id, arg):
        transaction = self.get_transaction_if_is_in_right_state(id, STATE_RES_REQ_SENT)
        body={"operation": OP_SITE_JOIN_FEDERATION_SEND_INFO, "argument": {"cpu": 10}}
        msg = DummyFedMessage(
           target=self._configuration["test.targetMessage"],
           body=body,
           bodyUriType=self._typetarget,
           id=id)
        self._ms.sendMessage(msg)
        print("Test actor sent info to Federator")


    def _join_federation_fail(self,applicant, id, arg):
        pass








