from abc import abstractmethod
from typing import TypeVar, Generic, Union, Type

PrimitiveType = TypeVar('PrimitiveType', int, str, float, bool)

CompatibleType = Union[PrimitiveType, 'PrimitiveValueObject']

PrimitiveValueObjectType = TypeVar('PrimitiveValueObjectType')


class PrimitiveValueObject(Generic[PrimitiveType]):
    @property
    @abstractmethod
    def value_type(self) -> Type[PrimitiveType]:
        pass

    def __init__(self, value: PrimitiveType):
        value = self._validate(value)
        self._value: PrimitiveType = value

    def __eq__(self, other: CompatibleType) -> bool:
        m = other
        if isinstance(other, PrimitiveValueObject):
            m = other._value
        return self._value == m

    def __hash__(self):
        return self._value.__hash__()

    def __le__(self, other: CompatibleType) -> bool:
        m = other
        if isinstance(other, PrimitiveValueObject):
            m = other._value
        return self._value <= m

    def __ge__(self, other: CompatibleType) -> bool:
        m = other
        if isinstance(other, PrimitiveValueObject):
            m = other._value
        return self._value >= m

    def __lt__(self, other: CompatibleType) -> bool:
        m = other
        if isinstance(other, PrimitiveValueObject):
            m = other._value
        return self._value < m

    def __gt__(self, other: CompatibleType) -> bool:
        m = other
        if isinstance(other, PrimitiveValueObject):
            m = other._value
        return self._value > m

    def __add__(self, other: CompatibleType) -> CompatibleType:
        m = other
        if isinstance(other, PrimitiveValueObject):
            m = other._value
        return self._value + m

    def __sub__(self, other: CompatibleType) -> CompatibleType:
        m = other
        if isinstance(other, PrimitiveValueObject):
            m = other._value
        return self._value - m

    def __mul__(self, other: CompatibleType) -> CompatibleType:
        m = other
        if isinstance(other, PrimitiveValueObject):
            m = other._value
        return self._value * m

    def __truediv__(self, other: CompatibleType) -> CompatibleType:
        m = other
        if isinstance(other, PrimitiveValueObject):
            m = other._value
        return self._value / m

    def serialize(self) -> PrimitiveType:
        return self._value

    @classmethod
    def deserialize(cls: Type[PrimitiveValueObjectType], value) -> PrimitiveValueObjectType:
        return cls(value)

    @classmethod
    def _validate(cls, value: object):
        if isinstance(value, cls.value_type):
            result = value
        elif isinstance(value, cls):
            result = value._value
        else:
            raise TypeError(f'Expect value of type ({cls.value_type.__name__}, {cls.__name__}), got {type(value)}')

        return result

    def __int__(self):
        return int(self._value)

    def __str__(self):
        return str(self._value)

    def __float__(self):
        return float(self._value)

    def __bool__(self):
        return bool(self._value)
