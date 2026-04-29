from fastapi import FastAPI
from .api.v1.router import router as inference_router

app = FastAPI()

app.include_router (
    inference_router,
    prefix="/api/v1"
)
