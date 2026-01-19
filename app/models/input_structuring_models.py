"""
Schema for Medical Entity Structuring Agent
"""

from typing import List
from pydantic import BaseModel, Field


class Input_Structuring_Output_Model(BaseModel):
    """Structured medical entities for coding"""
    
    icd_terms: List[str] = Field(
        ...,
        description="Diagnostic terms relevant for ICD-10-CM coding "
                    "(diseases, symptoms, conditions, findings)"
    )
    
    cpt_terms: List[str] = Field(
        ...,
        description="Procedure and service terms relevant for CPT-4 coding "
                    "(tests, imaging, evaluations, treatments)"
    )
    
    hcpcs_terms: List[str] = Field(
        ...,
        description="Supply, medication, and equipment terms relevant for "
                    "HCPCS Level II coding"
    )
