from contextvars import ContextVar

# Context variable to hold the Correlation ID for the current request context
correlation_id_ctx: ContextVar[str] = ContextVar("correlation_id", default="UNKNOWN")
