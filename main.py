from fastapi import FastAPI
from api.v1 import tts
from api.v1 import notes

app = FastAPI()

app.include_router(tts.router, prefix="/api/v1/tts", tags=["Text-to-Speech"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["Upload-file"])

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}



