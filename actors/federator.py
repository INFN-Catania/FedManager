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




import fed_logging
from fed_logging import *
import logging
from actors.abstract_classes import *
from actors.error import *
from federation_costants import *
from datetime import datetime, timedelta
logger = logging.getLogger("federation.core.federator")

TYPE_SITE_FEDMANAGER='ToSiteFedManager'

class FederationManager(Actor):
    """The actor responsible for the federation"""

    def __init__(self, messagescheduler, configuration):
        super(FederationManager, self).__init__(messagescheduler, "FederationManager", configuration)
        """Temporary type message to manage, for test purposes. A filter to rdf message will be implemented"""
        messagescheduler.registerActor("ToFederationManager", self)
        self._configuration = configuration

        self._fedoperations = {

            OP_SITE_JOIN_FEDERATION_REQUEST: {"handler": self._join_federation_request, OP_INIT_TRANSACTION: True},
            OP_SITE_JOIN_FEDERATION_SEND_INFO: {"handler": self._join_federation_send_info, OP_INIT_TRANSACTION: False}
        }
        self._federatedsites = {}

    def _add_federated_site(self, site, data):
        self._federatedsites[site] = data


    """O   P   E   R   A   T   I   O   N       H   A   N   D   L   E   R   S"""


    """J O I N  F E D E R A T I O N   H A N D L E R S"""

    """HANDLER for OP_SITE_JOIN_FEDERATION_REQUEST"""
    def _join_federation_request(self, applicant, id, arg):
        d = PrettyDictionary({'applicant': applicant, 'id': id, 'arg': arg})
        logger.debug ("Federation join  request received", d)


        """TODO: controllare che non ci siano transazioni attive di questo tipo per questo applicant"""
        """rispondi con SUCCESS e registra il nuovo sito"""
        self.registerTransaction(id=id,
                                 state=STATE_FEDERATOR_JOIN_REQUEST_SUCCESS,
                                 applicant=applicant,
                                 expiration_time=datetime.now() + timedelta(days=1),
                                 arg=arg)
        body={"operation": OP_FEDERATOR_JOIN_FEDERATION_SUCCESS, "argument": {"message": "ok"}}
        msg = DummyFedMessage(
           target=str(applicant),
           body=body,
           bodyUriType= TYPE_SITE_FEDMANAGER,
           id=id)
        self._ms.sendMessage(msg)
        d.update(PrettyDictionary({'msg': msg.toString()}))
        logger.debug("Federator send reply", d)



    """HANDLER for OP_SITE_JOIN_FEDERATION_SEND_INFO"""
    def _join_federation_send_info(self, applicant, id, arg):
        d = PrettyDictionary({'applicant': applicant, 'id': id, 'arg': arg})
        logger.debug('Federation join "send info"')
        #print ("Federation join send info  request received from " + applicant + " transaction ID: " + str(id) + "request: " + str(arg))

        self.get_transaction_if_is_in_right_state(id,applicant,STATE_FEDERATOR_JOIN_REQUEST_SUCCESS)
        transaction = self.getTransaction(id)
        """operazione di join eseguita registra sito"""
        logger.debug('Site joined federation',d)
        self._add_federated_site(applicant, arg)
        self.rmTransaction(id)


    """R E S O U R C E  R E Q U E S T   H A N D L E R S"""
    def _resource_request_request(self, applicant, id, arg):
        pass