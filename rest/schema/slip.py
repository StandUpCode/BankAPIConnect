from bson import ObjectId
from pydantic import BaseModel


class SlipVerifyRequest(BaseModel):
    slip_image: str

    class Config:
        schema_extra = {
            'example': {
                'buyer_id': str(ObjectId()),

            }
        }


class SlipVerifyResponse(BaseModel):
    transaction_ref_id: str

    class Config:
        schema_extra = {
            'example': {
                'transaction_ref_id': str(ObjectId()),
            }
        }
