from typing import TYPE_CHECKING, Union

from domain.base import StrIdValueObject


class QRData(StrIdValueObject):
    if TYPE_CHECKING:

        def __init__(self, id_: Union[str, "QRData"]):
            super().__init__(...)
