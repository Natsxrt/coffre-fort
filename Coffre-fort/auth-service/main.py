from fastapi import FastAPI
from db import init_db

app = FastAPI(root_path="/auth")
init_db()

@app.get("/health")
def health():
    return {"service": "auth"}