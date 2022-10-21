from typing import Union

from domain.base import PrimitiveValueObject


class SlipAmount(PrimitiveValueObject[int]):
    value_type = int

    def __init__(self, amount: Union[int, 'SlipAmount']):
        value: int = self._validate(amount)
        super().__init__(value)

    @classmethod
    def _validate(cls, value):
        value = super()._validate(value)

        if value < 0:
            raise ValueError(f'Expected SlipAmount >= 0, got {value}')

        return value
