from fastapi import FastAPI
from api.v1 import tts
from api.v1 import notes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tts.router, prefix="/api/v1/tts", tags=["Text-to-Speech"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["Upload-file"])

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}



