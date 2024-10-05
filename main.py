from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/load")
def read_load():
    return {"message": "Hello, World!"}


@app.get("/listen")
def read_listen(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
