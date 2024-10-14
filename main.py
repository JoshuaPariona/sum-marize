from fastapi import FastAPI
from api.v1 import tts
from api.v1 import notes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar orígenes permitidos (puedes agregar los que necesites)
origins = [
    "http://localhost",    # Para permitir desde localhost
    "http://localhost:5173",  # Si estás usando React o cualquier app en el puerto 3000
    "http://localhost:8000",  # Para tu API en el puerto 8000
    "http://127.0.0.1:8000"   # Variaciones de localhost
]

# Añadir el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

app.include_router(tts.router, prefix="/api/v1/tts", tags=["Text-to-Speech"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["Upload-file"])

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}



