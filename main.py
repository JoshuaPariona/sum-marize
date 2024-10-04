from fastapi import FastAPI

# Crear una instancia de FastAPI
app = FastAPI()

# Definir una ruta raíz
@app.get("/document")
def read_root():
    return {"message": "Hello, World!"}

# Definir otra ruta con un parámetro
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
