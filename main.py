from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables  
from app.product_router import router as product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Product API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(product_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Product API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "UP"
    }