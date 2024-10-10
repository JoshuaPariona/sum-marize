from fastapi import UploadFile, File
from fastapi import APIRouter
from typing import List

router = APIRouter()


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Procesar el archivo
    return {"filename": file.filename}
