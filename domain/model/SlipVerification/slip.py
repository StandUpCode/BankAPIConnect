from domain.base import Entity
from domain.base.model import Attribute
from .qrdata import QRData
from .slipStatus import SlipStatus
from .transaction_ref_id import TransactionRefId


class Slip(Entity):
    transaction_ref_id: TransactionRefId = Attribute(default=None)
    qr_data: QRData = Attribute()
    status: SlipStatus = Attribute(default=SlipStatus.Enum.WAITING)
    version: int = Attribute(default=0)
