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

__author__ = 'marco'

from actors.abstract_classes import *
from actors.error import *
from federation_costants import *
from datetime import datetime, timedelta

class FederationManager(Actor):
    """The actor responsible for the federation"""

    def __init__(self, messagescheduler, configuration):
        super(FederationManager, self).__init__(messagescheduler, "FederationManager", configuration)
        """Temporary type message to manage, for test purposes. A filter to rdf message will be implemented"""
        messagescheduler.registerActor("ToFederation", self)
        self._configuration = configuration

        self._fedoperations = {

            OP_SITE_JOIN_FEDERATION_REQUEST: {"handler": self._join_federation_request, OP_INIT_TRANSACTION: True},
            OP_SITE_JOIN_FEDERATION_SEND_INFO: {"handler": self._join_federation_send_info, OP_INIT_TRANSACTION: False}
        }
        self._federatedsites = {}



    """O P E R A T I O N   H A N D L E R S"""

    """HANDLER for OP_SITE_JOIN_FEDERATION_REQUEST"""
    def _join_federation_request(self, applicant, id, arg):
        print ("Federation join  request received from " + applicant + " transaction ID: " + str(id) + "request: " + str(arg))
        """TODO: controllare che non ci siano transazioni attive di questo tipo per questo applicant"""
        """rispondi con SUCCESS e registra il nuovo sito"""
        self.registerTransaction(id=id,
                                 state=STATE_FEDERATOR_JOIN_REQUEST_SUCCESS,
                                 applicant=applicant,
                                 expiration_time=datetime.now() + timedelta(days=1),
                                 arg=arg)
        body={"operation": OP_FEDERATOR_JOIN_FEDERATION_SUCCESS, "argument": {"message": "ok"}}
        msg = DummyFedMessage(
           target=self._configuration["test.targetMessage"],
           body=body,
           bodyUriType= "ToActor",
           id=id)
        self._ms.sendMessage(msg)
        print("federator sent: " + msg.toString())


    """HANDLER for OP_SITE_JOIN_FEDERATION_SEND_INFO"""
    def _join_federation_send_info(self, applicant, id, arg):
        print ("Federation join send info  request received from " + applicant + " transaction ID: " + str(id) + "request: " + str(arg))
        transaction = self.getTransaction(id)
        if transaction[APPLICANT] == applicant:
            if transaction[STATE] == STATE_FEDERATOR_JOIN_REQUEST_SUCCESS:
                """operazione di join eseguita registra sito"""
                print("site: " + applicant + " joined the federation")
                self._federatedsites[applicant] = arg
                self.rmTransaction(id)
            else:
                """gestisci l'errore manda risposta"""
                print("site: " + applicant + " is not in success state")
        else:
            """gestisci l'errore manda errore di risposta"""
            print("site: " + applicant + " has not active transaction")

