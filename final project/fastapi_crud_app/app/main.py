"""Application entry point.

Run with:
    uvicorn app.main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers import products

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A professional REST API with full CRUD operations for products.",
)

# Allow browsers from any origin to call the API (useful during development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """Create database tables automatically when the server starts."""
    init_db()


@app.get("/", tags=["Root"], summary="API information")
def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
    }


@app.get("/health", tags=["Root"], summary="Health check")
def health():
    return {"status": "ok"}


app.include_router(products.router)
