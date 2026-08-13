import time

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.api.v1 import api_v1_router
from app.core.config import settings
from app.core.context import correlation_id_ctx
from app.core.database import get_db
from app.core.logging import logger
from app.exceptions.handlers import register_exception_handlers
from app.services.analysis_service import generate_correlation_id

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
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def correlation_and_logging_middleware(request: Request, call_next):
    # Support both trace-id style Request-ID and custom Correlation-ID
    request_id = request.headers.get("X-Request-ID") or generate_correlation_id()
    cid = request.headers.get("X-Correlation-ID") or request_id

    correlation_id_ctx.set(cid)

    start_time = time.time()
    response = await call_next(request)
    duration_ms = int((time.time() - start_time) * 1000)

    response.headers["X-Correlation-ID"] = cid
    response.headers["X-Request-ID"] = request_id

    logger.info(
        f"[{cid}] {request.method} {request.url.path} - Status: {response.status_code} - Execution Time: {duration_ms}ms"
    )
    return response


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


@app.get("/health/live", tags=["Health"])
def health_live():
    """Liveness probe - indicates if the application is running."""
    return {"status": "alive"}


@app.get("/health/ready", tags=["Health"])
async def health_ready(db: AsyncSession = Depends(get_db)):
    """Readiness probe - indicates if the application is ready to accept traffic."""
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database not ready")
