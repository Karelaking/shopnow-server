from fastapi import FastAPI

app:FastAPI = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
