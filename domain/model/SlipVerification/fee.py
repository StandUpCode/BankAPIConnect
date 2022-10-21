from typing import Union

from domain.base import PrimitiveValueObject


class SlipFeeAmount(PrimitiveValueObject[int]):
    value_type = int

    def __init__(self, amount: Union[int, 'SlipFeeAmount']):
        value: int = self._validate(amount)
        super().__init__(value)

    @classmethod
    def _validate(cls, value):
        value = super()._validate(value)

        if value < 0:
            raise ValueError(f'Expected SlipFeeAmount >= 0, got {value}')

        return value
