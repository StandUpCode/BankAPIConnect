from fastapi import APIRouter, HTTPException, UploadFile, File

from domain import usecase

slip_api = APIRouter(prefix="/slip")

slip_api.post("/verify")


async def verify(slip_image_file: UploadFile = File(...), ):
    if slip_image_file is None:
        raise HTTPException(status_code=401, detail="silp cannot missing")
    try:
        file_content = await slip_image_file.read()
        result = await usecase.verify_silp(file=file_content)
        print(result)
    except Exception as err:
        raise HTTPException(status_code=500, detail="can't not read file content")
