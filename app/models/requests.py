"""
API Request Schemas
Request models for API endpoints
"""

from typing import Optional
from pydantic import BaseModel, Field


class ProcessTextRequest(BaseModel):
    """Request model for processing text-based medical report"""
    
    medical_report_text: str = Field(
        ...,
        min_length=10,
        description="The medical report text to process"
    )
    
    include_evaluation: bool = Field(
        default=True,
        description="Whether to include LLM judge evaluation"
    )


class ProcessPDFRequest(BaseModel):
    """Request model for PDF processing options"""
    
    include_evaluation: bool = Field(
        default=True,
        description="Whether to include LLM judge evaluation"
    )
