from fastapi import FastAPI, UploadFile, File
from typing import List

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Procesar el archivo
    return {"filename": file.filename}
