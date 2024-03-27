from fastapi import FastAPI
from app.utils.settings import settings

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/health")
async def root():
    return {"message": "Hi, The server is up and running"}
