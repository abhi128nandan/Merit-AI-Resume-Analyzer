from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.context import correlation_id_ctx
from app.core.logging import logger
from app.exceptions.custom_exceptions import ResumeAnalyzerException


def register_exception_handlers(app: FastAPI) -> None:
    """Registers custom exception handlers on the FastAPI application instance."""

    @app.exception_handler(ResumeAnalyzerException)
    async def custom_exception_handler(
        request: Request, exc: ResumeAnalyzerException
    ) -> JSONResponse:
        cid = correlation_id_ctx.get("UNKNOWN")
        logger.warning(
            f"[{cid}] Domain Exception: {exc.__class__.__name__} | "
            f"Endpoint: {request.url.path} | Status: {exc.status_code} | "
            f"Message: {exc.message} | Details: {exc.details}"
        )
        return JSONResponse(
            status_code=exc.status_code,
            headers={"X-Correlation-ID": cid},
            content={
                "error": {
                    "code": exc.__class__.__name__,
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        cid = correlation_id_ctx.get("UNKNOWN")
        logger.warning(
            f"[{cid}] Payload Validation Error | Endpoint: {request.url.path} | Status: 422 | Details: {exc.errors()}"
        )
        return JSONResponse(
            status_code=422,
            headers={"X-Correlation-ID": cid},
            content={
                "error": {
                    "code": "ValidationError",
                    "message": "This file is not a valid resume or document structure.",
                    "details": {"errors": exc.errors()},
                }
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        cid = correlation_id_ctx.get("UNKNOWN")
        logger.warning(
            f"[{cid}] HTTP Exception: {exc.status_code} | Endpoint: {request.url.path} | Detail: {exc.detail}"
        )
        message = (
            "The uploaded file exceeds the 5 MB limit."
            if exc.status_code == 413
            else (
                "The analysis timed out."
                if exc.status_code == 504
                else (
                    "This file is not a valid resume."
                    if exc.status_code == 422
                    else str(exc.detail)
                )
            )
        )
        return JSONResponse(
            status_code=exc.status_code,
            headers={"X-Correlation-ID": cid},
            content={
                "error": {
                    "code": f"HTTP_{exc.status_code}",
                    "message": message,
                    "details": None,
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        cid = correlation_id_ctx.get("UNKNOWN")
        logger.error(
            f"[{cid}] Unhandled Server Exception | Endpoint: {request.url.path} | Status: 500 | "
            f"Exception: {exc.__class__.__name__} | Error: {str(exc)}",
            exc_info=True,
        )
        return JSONResponse(
            status_code=500,
            headers={"X-Correlation-ID": cid},
            content={
                "error": {
                    "code": "InternalServerError",
                    "message": "Internal processing failed. Please try again.",
                    "details": None,
                }
            },
        )
