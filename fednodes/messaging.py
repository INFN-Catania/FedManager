from fednodes.abstract_classes import iConsumer
__author__ = 'maurizio'


class MessageScheduler(object):
    def __init__(self,producer,configuration):
        self._pr=producer
        self._configuration = configuration
        self._source = self._configuration["mom.consumer.topic"]
        self._actors = {}
    #from consumer
    def serveMessage(self, fedMessage):
        try:
            for actor in self._actors[fedMessage.getBodyUriType()]:
                actor.submitMessage(fedMessage)
        except KeyError:
            print("No actor available for message of type: '" +"'")

    #from Actors
    def sendMessage(self,fedMessage):
        fedMessage.setSource(self._source)
        self._pr.sendMessage(fedMessage)

    def registerActor(self,bodyUriType, actor):
        try:
            actorsForThisType = self._actors[bodyUriType]
            self._actors[bodyUriType].add(actor)
        except KeyError:
            """first actor for this Type"""
            self._actors[bodyUriType] = set([actor])


