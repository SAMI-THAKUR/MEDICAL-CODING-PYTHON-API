"""
HCPCS Coding Task

Defines the task responsible for assigning HCPCS Level II codes
from structured supply, drug, and equipment terms using a RAG-based workflow.
"""

from crewai import Task
from app.agents.hcpcs_coding_agent import HCPCS_Coding_Agent
from app.models.hcpcs_models import HCPCS_Coding_Output_Model


# =========================
# HCPCS Coding Task Definition
# =========================

# This task encapsulates the complete HCPCS Level II coding workflow:
# - Vector search retrieval
# - HCPCS code selection
# - ICD-10-CM medical necessity linkage
# - CMS and HCPCS Level II guideline enforcement
# - Structured output validation
HCPCS_Coding_Task = Task(
    # Human-readable task name for logging and observability
    name="HCPCS Coding Task",

    # Detailed instructions provided to the HCPCS coding agent
    description="""
    You are given a list of structured HCPCS-relevant terms along with
    associated ICD-10-CM diagnosis codes.

    Perform the following steps:

    1. Call the HCPCS_Vector_Search_Tool ONCE, passing the full list
       of HCPCS-relevant terms together.
    2. Review the retrieved HCPCS Level II candidates for each term.
    3. Select the most accurate and most specific HCPCS code
       for each medication, supply, or piece of equipment.
    4. If the retrieved HCPCS candidates do not contain the correct code
       or lack sufficient specificity, use your expert coding knowledge
       to provide the most accurate HCPCS Level II code.
    5. Link each selected HCPCS code to one or more ICD-10-CM diagnosis codes
       to justify its medical necessity.
    6. Apply official CMS and HCPCS Level II coding guidelines.
    7. Produce the final structured output.

    IMPORTANT:
    - Do NOT call the tool more than once.
    - Do NOT make repeated or per-term tool calls.
    - After receiving the tool output, return the final answer.
    """,

    # High-level description of the expected output
    expected_output=(
        "Structured HCPCS coding output conforming to the "
        "HCPCS_Coding_Output_Model model"
    ),

    # Agent responsible for executing this task
    agent=HCPCS_Coding_Agent,

    # Enforces strict schema validation of the task output
    output_pydantic=HCPCS_Coding_Output_Model
)
