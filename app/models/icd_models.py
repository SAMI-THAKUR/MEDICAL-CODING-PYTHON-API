"""
Schema for ICD-10-CM coding Agent
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ICD_Code(BaseModel):
    """Single ICD-10-CM code"""
    
    code: str = Field(..., description="Standardized ICD-10-CM code")
    
    description: Optional[str] = Field(
        None, description="Official description of the code"
    )
    
    confidence: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Model confidence score"
    )


class ICD_Coding_Output_Model(BaseModel):
    """ICD-10-CM coding output model"""
    
    icd_codes: List[ICD_Code] = Field(
        ..., description="List of ICD-10-CM diagnosis codes"
    )
