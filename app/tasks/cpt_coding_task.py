"""
CPT-4 Coding Task

Defines the task responsible for assigning CPT-4 codes
from structured procedure and service terms using a RAG-based workflow.
"""


# =========================
# Imports
# =========================

from crewai import Task
from app.agents.cpt_coding_agent import CPT_Coding_Agent
from app.models.cpt_models import CPT_Coding_Output_Model


# =========================
# CPT Coding Task Definition
# =========================

# This Task encapsulates the complete CPT coding workflow:
# - Vector search retrieval
# - CPT-4 code selection
# - ICD-10-CM linkage
# - AMA guideline compliance
# - Structured output generation
CPT_Coding_Task = Task(
    # Human-readable task name for logging, debugging, and tracing
    name="CPT Coding Task",

    # Detailed task instructions provided to the agent
    description="""
    You are given a list of structured procedure and service terms along with
    associated ICD-10-CM diagnosis codes.

    Perform the following steps:

    1. Call the CPT_Vector_Search_Tool ONCE, passing the full list
       of procedure and service terms together.
    2. Review the retrieved CPT-4 candidates for each term.
    3. Select the most accurate and most specific CPT code
       for each procedure or service.
    4. If the retrieved CPT candidates do not contain the correct code
       or lack sufficient specificity, use your expert CPT coding knowledge
       to provide the most accurate CPT-4 code.
    5. Link each selected CPT code to one or more ICD-10-CM diagnosis codes
       to justify medical necessity.
    6. Apply official AMA CPT-4 coding guidelines.
    7. Produce the final structured output.

    IMPORTANT:
    - Do NOT call the tool more than once.
    - Do NOT make repeated or per-term tool calls.
    - After receiving the tool output, return the final answer.
    """,

    # High-level description of what the final output should be
    expected_output=(
        "Structured CPT-4 coding output conforming to the "
        "CPT_Coding_Output_Model model"
    ),

    # The agent responsible for executing this task
    agent=CPT_Coding_Agent,

    # Enforces strict schema validation of the task output
    # Ensures predictable, machine-consumable CPT coding results
    output_pydantic=CPT_Coding_Output_Model
)
