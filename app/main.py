import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from app.api.v1.router import api_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(
        f"Starting {os.getenv('APP_NAME', 'FastAPI App')} "
        f"({os.getenv('ENVIRONMENT', 'development')})"
    )
    yield
    print(f"Stopping {os.getenv('APP_NAME', 'FastAPI App')}")


app = FastAPI(
    title=os.getenv("APP_NAME", "FastAPI App"),
    version=os.getenv("APP_VERSION", "0.1.0"),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "name": os.getenv("APP_NAME", "FastAPI App"),
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "docs": "/docs",
        "health": "/api/v1/health",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8001)),
        reload=os.getenv("DEBUG", "false").lower() == "true",
    )