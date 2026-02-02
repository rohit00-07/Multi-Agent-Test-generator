from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="AI Hiring Test Generator")

app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "OK"}

    