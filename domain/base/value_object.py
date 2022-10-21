from typing import TypeVar

from .model import Model

ImplementationType = TypeVar('ImplementationType', bound='ValueObject')


class ValueObject(Model):
    def __eq__(self: ImplementationType, other: ImplementationType):
        if type(self) is not type(other):
            return False

        for attr_name in getattr(self, '__attrs'):
            if getattr(self, attr_name) != getattr(other, attr_name):
                return False

        return True
