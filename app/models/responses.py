"""
API Response Schemas
Response models for API endpoints
"""

from token import OP
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class Medical_Coding_Response(BaseModel):
    """Medical coding response model"""
    
    extracted_entities: Dict
    icd_codes: Dict
    cpt_codes: Dict
    hcpcs_codes: Dict
    evaluation: Optional[Dict]


class HealthResponse(BaseModel):
    """Health check response"""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Environment name")
