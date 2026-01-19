"""
ICD-10-CM Coding Agent

Purpose:
--------
This agent assigns ICD-10-CM diagnosis codes using a
Retrieval-Augmented Generation (RAG) approach. It combines
vector-based ICD reference retrieval with expert ICD-10-CM
coding rules to ensure accuracy, specificity, and guideline compliance.
"""

# =========================
# Imports
# =========================
from crewai import Agent
from app.core.llm_config import kimi_k2
from app.agents.tools.icd_vector_search_tool import ICD_Vector_Search_Tool


# =========================
# ICD-10-CM Coding Agent Definition
# =========================

# This agent performs ICD-10-CM diagnosis code assignment.
# It is constrained to:
# - Use RAG for factual grounding
# - Apply official ICD-10-CM coding guidelines
# - Prefer highest available specificity
# - Output strictly validated JSON
ICD_Coding_Agent = Agent(
    # Human-readable role name for observability and audit logs
    role="ICD-10-CM Coding Agent",

    # Primary objective the agent must fulfill
    goal="Assign the most accurate and specific ICD-10-CM diagnosis codes using RAG",

    # Detailed system instructions defining expertise,
    # required behavior, and output constraints
    backstory="""
    You are a certified ICD-10-CM medical coding specialist.

    Input:
    - Structured diagnostic terms extracted from clinical text.

    You MUST:
    - Use the ICD vector search tool to retrieve relevant ICD-10 references
    - Apply ICD-10-CM official coding guidelines
    - Prefer highest specificity
    - Ignore negated or ruled-out diagnoses
    - If the retrieved ICD-10-CM candidates do not contain the correct code or
      lack sufficient specificity, use your expert medical coding knowledge to provide
      the most accurate and specific ICD-10-CM code.
    - Return ONLY valid JSON matching the ICD output schema
    """,

    # Tools the agent is explicitly allowed to use
    tools=[ICD_Vector_Search_Tool],

    # Rate limit to prevent excessive tool or LLM usage
    max_rpm=20,

    # Maximum reasoning / refinement iterations
    max_iter=5,

    # LLM instance used by this agent
    llm=kimi_k2,

    # Enables verbose logging for debugging and compliance audits
    verbose=True,

    # Prevents task delegation to other agents to ensure
    # all diagnosis coding decisions remain centralized
    allow_delegation=False
)
