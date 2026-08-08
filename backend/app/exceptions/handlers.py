from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.logging import logger
from app.exceptions.custom_exceptions import ResumeAnalyzerException


def register_exception_handlers(app: FastAPI) -> None:
    """Registers custom exception handlers on the FastAPI application instance."""

    @app.exception_handler(ResumeAnalyzerException)
    async def custom_exception_handler(
        request: Request, exc: ResumeAnalyzerException
    ) -> JSONResponse:
        logger.warning(
            f"Domain Exception Triggered: {exc.__class__.__name__} | "
            f"Path: {request.url.path} | Message: {exc.message} | "
            f"Details: {exc.details}"
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.__class__.__name__,
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.error(
            f"Unhandled Internal Server Error: {exc.__class__.__name__} | "
            f"Path: {request.url.path} | Error: {str(exc)}",
            exc_info=True,
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "InternalServerError",
                    "message": (
                        "An unexpected internal server error occurred. "
                        "Please try again later."
                    ),
                }
            },
        )
