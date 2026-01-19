"""
Health Check API Endpoint
"""

import os
from fastapi import APIRouter
from dotenv import load_dotenv

from app.models.responses import HealthResponse


# =========================
# Environment Configuration
# =========================

# Load environment variables from .env file (if present)
load_dotenv()


# =========================
# Router Definition
# =========================

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the API service is running"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        HealthResponse with service status
    """
    return HealthResponse(
        status="healthy",
        version=os.getenv("APP_VERSION", "0.1.0"),
        environment=os.getenv("ENVIRONMENT", "development"),
    )
