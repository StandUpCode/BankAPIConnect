from abc import ABC

from domain.base import RepositoryAbstract
from domain.model.SlipVerification.slip import Slip
from domain.model.SlipVerification.transaction_ref_id import TransactionRefId


class SlipRepositoryAbstract(RepositoryAbstract[TransactionRefId, Slip], ABC):
    pass
