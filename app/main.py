from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="AI ML Capstone Project",
    description="Generative AI powered enterprise document question-answering system",
    version="1.0.0"
)

app.include_router(router)