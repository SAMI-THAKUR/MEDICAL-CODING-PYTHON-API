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


class Section_Judgement(BaseModel):
    """Section-level evaluation"""
    
    section: str = Field(..., description="icd | cpt | hcpcs")
    verdict: Verdict
    
    # ✅ NEW FIELD
    incorrect_codes: Optional[List[str]] = Field(
        default=None,
        description="Codes that are wrongly included or should not be present based on the documentation"
    )
    
    notes: Optional[str] = None


class Medical_Coding_Judge_Output(BaseModel):
    """Complete judge evaluation output"""
    
    overall_verdict: Verdict
    
    overall_score: float = Field(
        ..., ge=0.0, le=1.0, description="Overall quality score"
    )
    
    section_judgements: List[Section_Judgement]
    
    compliance_risk: Risk_Level
    
    summary: str = Field(
        ..., min_length=30,
        description="Concise explanation of the final judgement"
    )
    
    # ✅ OPTIONAL: overall incorrect codes summary
    incorrect_codes_overall: Optional[List[str]] = Field(
        default=None,
        description="All incorrectly included codes across sections"
    )
    
    notes: Optional[str] = None