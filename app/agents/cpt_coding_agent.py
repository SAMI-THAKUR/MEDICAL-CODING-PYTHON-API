"""
CPT-4 Coding Agent

Purpose:
--------
This agent is responsible for assigning CPT-4 procedure and service codes
using a Retrieval-Augmented Generation (RAG) approach. It combines vector-based
CPT reference retrieval with expert-level CPT coding rules to ensure accuracy,
specificity, and AMA guideline compliance.
"""

# =========================
# Imports
# =========================
from crewai import Agent
from app.core.llm_config import gpt_oss_120
from app.agents.tools.cpt_vector_search_tool import CPT_Vector_Search_Tool


# =========================
# CPT-4 Coding Agent Definition
# =========================

# This agent performs CPT-4 code selection and validation.
# It is constrained to:
# - Use RAG (vector search) for grounding
# - Apply AMA CPT-4 guidelines
# - Produce strictly structured output
CPT_Coding_Agent = Agent(
    # Human-readable role name for traceability and logging
    role="CPT-4 Coding Agent",

    # High-level objective the agent must achieve
    goal="Assign the most accurate CPT-4 procedure and service codes using RAG",

    # Detailed system-level instructions defining expertise,
    # inputs, required behavior, and output constraints
    backstory="""
    You are a certified CPT-4 medical coding specialist.

    Input:
    - Structured procedure and service terms
    - Associated ICD-10-CM diagnosis codes for medical necessity context

    You MUST:
    - Use the CPT vector search tool to retrieve relevant CPT references
    - Apply official CPT-4 and AMA coding guidelines
    - Avoid unbundling and incorrect procedure hierarchy
    - Select the most accurate and specific CPT code
    - If retrieved CPT candidates do not contain the correct code or
      lack sufficient specificity, use your expert CPT coding knowledge
      to provide the most accurate CPT-4 code
    - Link each CPT code to one or more ICD-10-CM codes
    - Return ONLY structured output conforming to the CPT output schema
    """,

    # Tools the agent is allowed to use during execution
    tools=[CPT_Vector_Search_Tool],

    # Rate limit to control external API usage and prevent over-calling
    max_rpm=20,

    # Maximum number of reasoning / execution iterations
    max_iter=5,

    # Large Language Model configuration used by this agent
    llm=gpt_oss_120,

    # Enables detailed execution logs for debugging and audits
    verbose=True,

    # Disables delegation to ensure all coding decisions
    # are made solely by this certified CPT agent
    allow_delegation=False
)
