from typing import TYPE_CHECKING, Union

from domain.base import StrIdValueObject


class TransactionRefId(StrIdValueObject):
    if TYPE_CHECKING:
        def __init__(self, id_: Union[str, "TransactionRefId"]):
            super().__init__(...)
