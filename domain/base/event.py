from abc import ABC, abstractmethod

from .model import Model


class DomainEvent(Model):
    @classmethod
    def event_name(cls):
        return cls.__name__

    def __eq__(self, other: 'DomainEvent'):
        if type(self) is not type(other):
            return False
        return self.serialize() == other.serialize()


class DomainEventPublisher(ABC):
    @abstractmethod
    def publish(self, event: DomainEvent):
        pass


class DummyEventPublisher(DomainEventPublisher):
    def __init__(self):
        self.events = []

    def publish(self, event: DomainEvent):
        self.events.append(event)
