from typing import Union, TypeVar, Generic, TYPE_CHECKING

from .primitive_value_object import PrimitiveValueObject


ImplementationType = TypeVar('ImplementationType', bound='StrIdValueObject')


class StrIdValueObject(PrimitiveValueObject[str]):
    value_type = str

    if TYPE_CHECKING:
        def __init__(self: ImplementationType, id_: Union[str, ImplementationType]):
            super().__init__(id_)