"""
Medical Entity Structuring Agent

Purpose:
--------
This agent extracts, normalizes, and structures medically relevant entities
from raw clinical or prescription text. Its output serves as the upstream
input for ICD-10-CM, CPT-4, and HCPCS Level II coding agents.
"""

# =========================
# Imports
# =========================

from crewai import Agent
from app.core.llm_config import gemini_2_5_flash


# =========================
# Medical Entity Structuring Agent Definition
# =========================

# This agent acts as a medical coding pre-processor.
# It converts unstructured clinical content into
# standardized, coding-ready entities.
Input_Structuring_Agent = Agent(
    # Human-readable role name for observability and tracing
    role="Medical Entity Structuring Agent",

    # High-level objective of the agent
    goal="Convert raw medical prescription content into coding-ready structured entities",

    # System-level instructions defining responsibilities,
    # input scope, and output constraints
    backstory="""
    You are a medical coding pre-processor.
    You receive medical prescription content that may include:
    - Diagnoses or clinical impressions
    - Prescribed medications (drug name, dose, route, frequency)
    - Injections, infusions, or administered drugs
    - Procedures or services performed during the encounter
    - Clinically relevant findings that directly impact treatment

    Your responsibility is to analyze the prescription and
    extract, normalize, and categorize medically relevant information
    into coding-ready terms suitable for:
    - ICD-10-CM (diagnoses and clinically relevant conditions)
    - CPT-4 (procedures, evaluations, administrations)
    - HCPCS Level II (medications, injections, supplies, DME)

    Return ONLY structured output conforming to the
    Structured_Medical_Entities model.
    """,

    # Rate limit kept intentionally low to reduce hallucination
    # and encourage deliberate extraction behavior
    max_rpm=2,

    # Maximum reasoning / refinement iterations
    max_iter=5,

    # Enables verbose execution logs for debugging and audits
    verbose=True,

    # Prevents delegation to ensure a single, deterministic
    # entity extraction path
    allow_delegation=False,

    # LLM configuration optimized for structured extraction tasks
    llm=gemini_2_5_flash
)
