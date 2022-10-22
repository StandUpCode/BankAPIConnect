from fastapi import APIRouter, HTTPException, UploadFile, File

from Config.SCBConfig import SCBConfig
from adapter.model.BankAPI import SCBAPI_Service
from utils.imagehandler import ImageHandler
from utils.slip import SlipQRData

slip_api = APIRouter()

SCBAPI_Service = SCBAPI_Service(SCBConfig())


# KBankAPI_Service = KBankAPI_Service(KBankConfig())


@slip_api.post("/scb/verify")
async def verify_scb(slip_image_file: UploadFile = File(...), ):
    if slip_image_file is None:
        raise HTTPException(status_code=401, detail="silp cannot missing")

    file_content = await slip_image_file.read()
    print(slip_image_file.filename)

    image = ImageHandler.formfile_to_pillow_image(file_content)
    slip = SlipQRData.create_from_image(image)
    print(slip.payload.transaction_ref_id, slip.payload.sending_bank_id)
    result = await SCBAPI_Service.verify_slip(
        transaction_ref_id=slip.payload.transaction_ref_id,
        sending_bank_id=slip.payload.sending_bank_id
    )
    print(result)
