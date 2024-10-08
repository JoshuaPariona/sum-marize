from typing import Dict

from fastapi import APIRouter, File, UploadFile

from core.notes_processor import \
    process_notes_file  # Asegúrate de que la importación sea correcta

router = APIRouter()

@router.post("/process_notes/")
async def process_notes(file: UploadFile = File(...)) -> Dict:
    # Procesar el archivo CSV subido
    processed_data = await process_notes_file(file)
    return {"status": "success", "notes": processed_data}
