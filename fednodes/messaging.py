#from fednodes.abstract_classes import iConsumer
__author__ = 'maurizio'
#from fednodes.dummy_classes import DummyFedMessage
import fed_logging
from fed_logging import *
import logging
logger = logging.getLogger("federation.core.federator")


class MessageScheduler(object):
    def __init__(self, message_class, producer,configuration):
        self._pr=producer
        self._configuration = configuration
        self._source = self._configuration["mom.consumer.topic"]
        self._actors = {}
        self._messageClass = message_class


    """from consumer
    fedStringMessage is a string containing the message encoded by a particular codification (rdf, simple,...)
    """
    def serveMessage(self, fedStringMessage):
        try:
            try:
                fedMessage=self._messageClass.createMessageFromString(fedStringMessage)
            except Exception as err:
                logger.error("Error creating the message",PrettyDictionary({'exception': err}))
                return
            for actor in self._actors[fedMessage.getBodyUriType()]:
                actor.submitMessage(fedMessage)
        except KeyError:
            #print("No actor available for message of type: '" + fedMessage.getBodyUriType())
            logger.error("No actor available for message of this type",PrettyDictionary({'type': fedMessage.getBodyUriType()}))
        except Exception as err:
            """TODO: create an Error Manager"""
            logger.error("Error from actor",PrettyDictionary({'exception': err}))
    """from Actors
    fedMessage is a python object encapsulating the message information
    """
    def sendMessage(self,fedMessage):
        fedMessage.setSource(self._source)
        msg=fedMessage.toString()
        self._pr.sendMessage(msg,fedMessage.getTarget())


    def registerActor(self,bodyUriType, actor):
        try:
            actorsForThisType = self._actors[bodyUriType]
            self._actors[bodyUriType].add(actor)
        except KeyError:
            """first actor for this Type"""
            self._actors[bodyUriType] = set([actor])


