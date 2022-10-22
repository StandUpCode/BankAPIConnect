from enum import Enum

from pydantic.types import constr


class GetBankCode(Enum):
    BOT = "001"
    BBL = "002"
    KBANK = "004"
    KTB = "006"
    TTB = "011"
    SCB = "014"
    CIMBT = "022"
    UOBT = "024"
    BAY = "025"
    GSB = "030"
    GHB = "033"
    BAAC = "034"
    ISBT = "066"
    KKP = "069"
    TCD = "071"
    LHB = "073"


AnyBankCode = constr(min_length=3, max_length=3)
