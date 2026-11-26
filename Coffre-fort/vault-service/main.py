from fastapi import FastAPI

app = FastAPI(root_path="/vault")

@app.get("/health")
def health():
    return {"service": "vault"}