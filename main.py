from fastapi import FastAPI
from api.v1 import tts

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

app.include_router(tts.router, prefix="/api/v1/tts", tags=["Text-to-Speech"])