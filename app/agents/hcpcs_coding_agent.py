"""
HCPCS Level II Coding Agent

Purpose:
--------
This agent assigns HCPCS Level II codes for supplies, drugs,
durable medical equipment (DME), and non-physician services
using a Retrieval-Augmented Generation (RAG) approach.
"""

# =========================
# Imports
# =========================

from crewai import Agent
from app.core.llm_config import xiaomi_mimo_v2_flash
from app.agents.tools.hcpcs_vector_search_tool import HCPCS_Vector_Search_Tool


# =========================
# HCPCS Level II Coding Agent Definition
# =========================

# This agent is responsible for selecting HCPCS Level II codes
# while enforcing CMS and HCPCS coding rules.
HCPCS_Coding_Agent = Agent(
    # Human-readable role name for logging and audit trails
    role="HCPCS Level II Coding Agent",

    # Primary objective of the agent
    goal="Assign the most accurate HCPCS Level II codes for supplies, drugs, and equipment using RAG",

    # System-level instructions defining expertise, inputs,
    # behavioral constraints, and output requirements
    backstory="""
    You are a certified HCPCS Level II medical coding specialist.

    Input:
    - Structured HCPCS-relevant terms (medications, supplies, DME, injections)
    - Associated ICD-10-CM diagnosis codes for medical necessity context

    You MUST:
    - Use the HCPCS vector search tool to retrieve relevant HCPCS references
    - Link each HCPCS code to one or more ICD-10-CM codes to justify medical necessity
    - Apply official HCPCS Level II and CMS coding guidelines
    - Distinguish drugs, supplies, DME, and non-physician services correctly
    - If retrieved HCPCS candidates do not contain the correct code or
      lack sufficient specificity, use your expert HCPCS coding knowledge
      to provide the most accurate Level II code
    - Return ONLY structured output conforming to the HCPCS output schema
    """,

    # Tools explicitly allowed for this agent
    tools=[HCPCS_Vector_Search_Tool],

    # Rate limiting to control LLM and tool usage
    max_rpm=20,

    # Maximum reasoning / refinement iterations
    max_iter=5,

    # LLM configuration used for HCPCS coding
    llm=xiaomi_mimo_v2_flash,

    # Enables verbose execution logs for debugging and compliance review
    verbose=True,

    # Prevents delegation to ensure all HCPCS decisions
    # are made by this specialized agent
    allow_delegation=False
)
