"""
Schema for HCPCS Level II coding Agent
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class HCPCS_Code(BaseModel):
    """Single HCPCS Level II code"""
    
    code: str = Field(
        ..., description="HCPCS Level II code (e.g., J, A, E, Q, G codes)"
    )
    
    description: Optional[str] = Field(
        None, description="Official HCPCS description of the supply, drug, or service"
    )
    
    linked_icd_codes: List[str] = Field(
        ...,
        description="List of ICD-10-CM diagnosis codes that justify the medical necessity "
                    "of this HCPCS code"
    )
    
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Model confidence score"
    )


class HCPCS_Coding_Output_Model(BaseModel):
    """HCPCS Level II coding output model"""
    
    hcpcs_codes: List[HCPCS_Code] = Field(
        ..., description="List of HCPCS Level II codes linked to ICD-10 diagnoses"
    )
