"""
API v1 Endpoints Module
"""

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.coding import router as coding_router

__all__ = ["health_router", "coding_router"]
