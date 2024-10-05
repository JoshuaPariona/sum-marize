from fastapi import UploadFile, File
from fastapi import APIRouter
from typing import List

router = APIRouter()

@router.post("/process_notes/")
async def process_notes(file: UploadFile = File(...)):
    # Lógica para convertir a JSON y clasificar
    return {"status": "success", "notes": file.processed_notes}
