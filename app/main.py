from fastapi import FastAPI

app = FastAPI(title="TrialLens", version="0.1.0")


@app.get("/check")
def check():
    return {"status": "ok"}
