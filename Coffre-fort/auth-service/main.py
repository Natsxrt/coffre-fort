from fastapi import FastAPI

app = FastAPI(root_path="/auth")

@app.get("/health")
def health():
    return {"service": "auth"}