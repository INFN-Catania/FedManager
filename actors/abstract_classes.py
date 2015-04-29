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
from error import *
from federation_costants import *
from fednodes.dummy_classes import DummyFedMessage
import uuid
import fed_logging
from fed_logging import *
import logging
import traceback
STATE="state"
ETIME="expiration_time"
ARG="argument"
APPLICANT="applicant"

logger = logging.getLogger("federation.core.federator")

class Actor():
    __metaclass__ = ABCMeta
    """An Abstract class in which are pointed out the methods each actor must implement"""
    def __init__(self, messagescheduler, name, configuration):
        self._ms = messagescheduler
        self._configuration = configuration
        self._name = name
        """Map where actor store the active transactions
        key UUID : {state,applicant,expirationtime,arg}"""
        self._transactions = {}
        self._messageHandlers = {
            DummyFedMessage: self._dummymessagehandler
        }



    """return UUID of new transaction"""
    def createTransaction(self, state, applicant, expiration_time, arg):
        id=uuid.uuid4()
        if id in self._transactions:
            raise TransactionAlreadyExist("Unexpected error on Transaction creation")
        self._transactions[id] = {STATE: state, APPLICANT:applicant, ETIME: expiration_time, ARG: arg}
        return id

    """return UUID of registered transaction (the same passed as parameter)"""
    def registerTransaction(self, id, state, applicant, expiration_time, arg):
        if id in self._transactions:
            raise TransactionAlreadyExist("Transaction already present")
        self._transactions[id] = {STATE: state, APPLICANT: applicant, ETIME: expiration_time, ARG: arg}

        logger.debug("Transaction registered", PrettyDictionary({'transactionid': id,'state': state, 'applicant': applicant, 'arg': arg}))

        return id

    """state_time is a dictonary {state, expiration_time}
    return old data"""
    def updateTransaction(self, id, state_time, arg):
        data = self._transactions[id]
        self._transactions[id] = state_time,id
        return data

    def getTransaction(self,id):
        """

        :rtype : transaction as dictionary
        """
        return self._transactions[id]

    def existTransaction(self,id):
        return id in self._transactions

    def rmTransaction(self,id):
        data = self._transactions[id]
        self._transactions[id]
        return data


    def get_transaction_if_is_in_right_state(self, id, applicant, state):
        trans = self.getTransaction(id)
        if trans[STATE] != state or trans[APPLICANT] != applicant:
            raise TransactionNotInRightState('Wrong state: ' + trans[STATE] + 'for applicant: ' + applicant)
        return trans


    """Method invoked by messaging system to delivery message to Actor
    message is a python object"""
    def submitMessage(self, fedMessage):
        try:

            logger.debug("Received message: " , PrettyDictionary({'type body message': fedMessage.getBodyUriType(),
                                                                  'type message': type(fedMessage)}))
            self._messageHandlers[type(fedMessage)](fedMessage)
        except KeyError as e:
            raise ActorException("Unknow message type" + str(type(fedMessage)))
        except Exception as e:
            out = StringIO.StringIO()
            traceback.print_exc(file=out)
            logger.debug('Error in actor: ', PrettyDictionary({'name': self._name,'error':out.getvalue()}))
            raise e
    """M E S S A G E  H A N D L E R S"""

    """Handler for dummymessage."""
    def _dummymessagehandler(self, fedmessage):
        body = fedmessage.getBody()
        try:
            operation = body["operation"]
            opDict = self._fedoperations[operation]
            if  opDict[OP_INIT_TRANSACTION] == (not self.existTransaction(fedmessage.getId())):
                opDict["handler"](applicant=fedmessage.getSource(),
                                  id=fedmessage.getId(),
                                  arg=body["argument"])
            else:
                #logger.error("Operation is invalid: or Transaction already exist and operation is an initial operation or viceversa")
                raise OperationInvalidInThisState("Operation is invalid: or Transaction already exist and operation is an initial operation or viceversa")

        except KeyError:
            logger.error("Unknow message",PrettyDictionary({'body message': body}))


    """Handler for message with rdf/owl content"""
    def _rdfmessagehandler(self, fedmessage):
        pass