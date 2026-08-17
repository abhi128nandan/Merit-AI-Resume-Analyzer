from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint to verify system status."""
    return {"status": "healthy", "version": "v1"}
