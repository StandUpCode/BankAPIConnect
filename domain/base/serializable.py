from abc import ABC, abstractmethod


class Serializable(ABC):
    @abstractmethod
    def serialize(self):
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, value):
        pass
