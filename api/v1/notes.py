from fastapi import FastAPI, UploadFile, File
from typing import List

app = FastAPI()


@app.post("/process_notes/")
async def process_notes(file: UploadFile = File(...)):
    # Lógica para convertir a JSON y clasificar
    return {"status": "success", "notes": processed_notes}
