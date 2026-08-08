from fastapi import FastAPI

from app.api.v1 import api_v1_router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions.handlers import register_exception_handlers

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for AI Resume Analyzer",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register central exception handlers
register_exception_handlers(app)

# Register API routers
app.include_router(api_v1_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs": "/docs",
        "api_v1": settings.API_V1_STR,
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
