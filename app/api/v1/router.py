"""
API v1 Router Configuration
Combines all v1 routes
"""

from fastapi import APIRouter
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.coding import router as coding_router

# Create main v1 router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    health_router,
    tags=["Health"]
)

api_router.include_router(
    coding_router,
    prefix="/coding",
    tags=["Medical Coding"]
)
