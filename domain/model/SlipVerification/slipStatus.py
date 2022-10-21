from enum import Enum
from typing import TYPE_CHECKING, Union

from domain.base import PrimitiveValueObject


class SlipStatusEnum(str, Enum):
    WAITING = 'waiting'
    VALIDATED = 'validated'

    @classmethod
    def has_value(cls, value):
        return value in cls._member_map_.values()


class SlipStatus(PrimitiveValueObject[str]):
    value_type = str
    Enum = SlipStatusEnum

    def is_validated(self) -> bool:
        return self._value == SlipStatusEnum.VALIDATED

    def is_waiting(self) -> bool:
        return self._value == SlipStatusEnum.WAITING

    @classmethod
    def _validate(cls, status):
        if isinstance(status, SlipStatusEnum):
            status = status.value
        value = super()._validate(status)

        if not SlipStatusEnum.has_value(value):
            raise ValueError(f'SlipStatus named "{value}" not exists')

        return value

    if TYPE_CHECKING:
        def __init__(self, status: Union[str, 'SlipStatus']):
            super().__init__(...)
