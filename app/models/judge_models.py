"""
Schema for LLM as a Judge Agent
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class Verdict(str, Enum):
    """Pass/fail verdict"""
    pass_ = "pass"
    fail = "fail"


class Support_Level(Enum):
    """Documentation support level"""
    HALLUCINATED = 0
    PARTIALLY_SUPPORTED = 1
    FULLY_SUPPORTED = 2


class Risk_Level(str, Enum):
    """Compliance risk level"""
    low = "low"
    medium = "medium"
    high = "high"


class Code_Judgement(BaseModel):
    """Individual code evaluation"""
    
    code: str = Field(..., description="ICD, CPT, or HCPCS code")
    
    code_type: str = Field(..., description="icd | cpt | hcpcs")
    
    term_match: bool = Field(
        ..., description="Code matches extracted clinical term"
    )
    
    documentation_support: Support_Level
    
    linkage_valid: Optional[bool] = Field(
        None,
        description="Whether linked ICD codes justify this code"
    )
    
    confidence_alignment: bool = Field(
        ..., description="Model confidence aligns with correctness"
    )
    
    issues: Optional[List[str]] = Field(
        default=None,
        description="Reasons for failure or concern"
    )


class Section_Judgement(BaseModel):
    """Section-level evaluation"""
    
    section: str = Field(..., description="icd | cpt | hcpcs")
    verdict: Verdict
    notes: Optional[str] = None


class Medical_Coding_Judge_Output(BaseModel):
    """Complete judge evaluation output"""
    
    overall_verdict: Verdict
    
    overall_score: float = Field(
        ..., ge=0.0, le=1.0, description="Overall quality score"
    )
    
    section_judgements: List[Section_Judgement]
    
    code_judgements: List[Code_Judgement]
    
    compliance_risk: Risk_Level
    
    summary: str = Field(
        ..., min_length=30,
        description="Concise explanation of the final judgement"
    )
    
    notes: Optional[str] = None
