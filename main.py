from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables  
from app.router.user_router import router as user_router
from app.router.product_router import router as product_router
from app.router.admin_router import router as admin_router


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
app.include_router(user_router)
app.include_router(admin_router)


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