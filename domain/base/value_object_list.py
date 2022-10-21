from abc import abstractmethod
from typing import TypeVar, Generic, Union, Type, List

from .model import validate

ValueType = TypeVar('ValueType')

ValueObjectListType = TypeVar('ValueObjectListType')

CompatibleType = Union[ValueType, 'ValueObjectList']


class ValueObjectList(Generic[ValueType]):
    @property
    @abstractmethod
    def value_type(self) -> ValueType:
        pass

    def __init__(self: ValueObjectListType, values: Union[List[ValueType], ValueObjectListType]):
        values = self._validate(values)
        self._values: List[ValueType] = values

    def _validate(self, values) -> List[ValueType]:
        return [validate(v, self.value_type) for v in values]

    def __iter__(self):
        yield from self._values

    def __eq__(self, other: CompatibleType) -> bool:
        m = other
        if isinstance(other, ValueObjectList):
            m = other._values
        return self._values == list(m)

    def __hash__(self):
        return tuple(self._values).__hash__()

    def serialize(self) -> List[ValueType]:
        return [v.serialize() for v in self._values]

    @classmethod
    def deserialize(cls: Type[ValueObjectListType], values: List[ValueType]) -> ValueObjectListType:
        return cls([cls.value_type.deserialize(v) for v in values])
