from fastapi import FastAPI
from app.api.api_routes import api_router
from app.cron.cron_routes import cron_router
from app.db import shutdown, startup
from app.utils.settings import settings

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/health")
async def root():
    return {"message": "Hi, The server is up and running"}


app.include_router(cron_router, prefix="v1/cron")
app.include_router(api_router, prefix="v1/api")


@app.on_event("startup")
async def startup_event():
    await startup()


@app.on_event("shutdown")
async def shutdown_event():
    await shutdown()
