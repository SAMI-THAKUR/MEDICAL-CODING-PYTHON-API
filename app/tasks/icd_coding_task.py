"""
ICD-10-CM Coding Task

Defines the task responsible for assigning ICD-10-CM diagnosis codes
from structured diagnostic terms using a RAG-based workflow.
"""

# =========================
# Imports
# =========================
from crewai import Task
from app.agents.icd_coding_agent import ICD_Coding_Agent
from app.models.icd_models import ICD_Coding_Output_Model


# =========================
# ICD-10-CM Coding Task Definition
# =========================

# This task encapsulates the complete ICD-10-CM coding workflow:
# - Vector search retrieval
# - Diagnosis code selection
# - Guideline enforcement
# - Structured output validation
ICD_Coding_Task = Task(
    # Human-readable task name for logging and observability
    name="ICD-10-CM Coding Task",

    # Detailed instructions provided to the ICD coding agent
    description="""
    You are given a list of structured diagnostic terms for ICD-10-CM coding.

    Perform the following steps:

    1. Call the ICD_Vector_Search_Tool ONCE, passing the full list
       of diagnostic terms together.
    2. Review the retrieved ICD-10-CM candidates for each term.
    3. Select the most accurate and most specific ICD-10-CM code
       for each diagnostic term.
    4. If the retrieved ICD-10-CM candidates do not contain the correct code
       or lack sufficient specificity, use your expert medical coding
       knowledge to provide the most accurate and specific ICD-10-CM code.
    5. Apply official ICD-10-CM coding guidelines.
    6. Produce the final structured output.

    IMPORTANT:
    - Do NOT call the tool more than once.
    - Do NOT make repeated or per-term tool calls.
    - After receiving the tool output, return the final answer.
    """,

    # High-level description of the expected output
    expected_output=(
        "Structured ICD-10-CM coding output conforming to the "
        "ICD_Coding_Output_Model model"
    ),

    # Agent responsible for executing this task
    agent=ICD_Coding_Agent,

    # Enforces strict schema validation of the task output
    output_pydantic=ICD_Coding_Output_Model
)
