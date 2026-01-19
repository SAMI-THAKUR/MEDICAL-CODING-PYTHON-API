"""
Input Structuring Task

Defines the task responsible for extracting and structuring
billing-relevant medical entities from raw clinical encounter text.
"""

from crewai import Task
from app.agents.input_structuring_agent import Input_Structuring_Agent
from app.models.input_structuring_models import Input_Structuring_Output_Model


# =========================
# Input Structuring Task Definition
# =========================

# This task performs deterministic medical entity extraction and normalization.
# It produces coding-ready terms for downstream ICD-10-CM, CPT-4,
# and HCPCS Level II coding agents.
Input_Structuring_Task = Task(
    # Human-readable task name for tracing and observability
    name="Input Structuring Task",

    # Detailed extraction instructions and strict normalization rules
    description="""
    You are a medical coding entity extraction engine.

    Process the following clinical encounter text:
    {medical_report_text}

    Your task is to extract **billing-relevant medical concepts** and organize
    them into the correct U.S. medical coding categories.

    ────────────────────────────────────────
    OUTPUT STRUCTURE (MANDATORY)

    Return THREE distinct structured lists:

    1. ICD-10-CM Diagnostic Terms
    2. CPT-4 Procedure / Service Terms
    3. HCPCS Level II Terms (Drugs, Supplies, DME)

    Return **terms only** (no codes, no explanations).

    ────────────────────────────────────────
    EXTRACTION RULES (STRICT)

    ### 1. ICD-10-CM Diagnostic Terms
    Extract conditions that meet ALL of the following:
    - Explicitly documented as a diagnosis or assessment
    - Not negated, denied, ruled out, or listed only as a possibility
    - Clinically relevant to the current encounter

    Include:
    - Acute or chronic diseases
    - Active conditions being treated
    - Relevant historical conditions when documented as ongoing or impacting care

    Exclude:
    - Symptoms that are part of a confirmed diagnosis
    - Normal exam findings
    - Screening statements without a diagnosis

    If no diagnosis is documented, extract **standalone symptoms** only.

    Normalize abbreviations and shorthand to full clinical terms.

    ---

    ### 2. CPT-4 Procedure / Service Terms
    Extract **only services that were actually performed during this encounter**,
    including:
    - Evaluation & management services
    - Laboratory tests performed
    - Imaging studies completed
    - Therapeutic procedures (e.g., infusions, injections)

    Exclude:
    - Planned, ordered, or future services
    - Patient education or counseling alone
    - Clinical observations without an associated service

    Normalize descriptions to standard medical procedure terminology.

    ---

    ### 3. HCPCS Level II Terms
    Extract **non-CPT billable items** that were **administered or provided during
    the encounter**, including:
    - Injectable or infused medications
    - Supplies or biological agents
    - Durable medical equipment provided

    Include:
    - Medication name
    - Route of administration
    - Strength or dose when documented

    Exclude:
    - Oral medications that were only prescribed for home use
    - Home medications not administered during the visit

    ────────────────────────────────────────
    GENERAL NORMALIZATION RULES
    - Ignore negated or irrelevant concepts
    - Do not duplicate terms across categories
    - Prefer specific diagnoses over vague findings
    - Ensure each term clearly belongs to only one category
    - Use medically standard terminology

    ────────────────────────────────────────
    TERMINOLOGY PRECISION RULES (MANDATORY)

    When extracting terms:

    1. CPT-4 Terminology Precision
    - Use conservative, minimally sufficient terminology.
    - Do NOT assume higher specificity unless explicitly documented.
    - If a test or procedure type is unclear:
      - Prefer general terms (e.g., “urinalysis, non-automated” rather than
        “urinalysis with microscopy”).
    - Only include qualifiers such as “with microscopy,” “automated,” “complex,”
      or “extended” if explicitly stated in the clinical text.

    2. E/M Service Terminology
    - Extract E/M services at the category level only.
    - Do NOT infer visit level or complexity.
    - Use setting-neutral phrasing unless clearly documented.

    3. HCPCS Medication Terminology
    - Normalize medications using:
      Drug name + route + strength
    - If administered via IV, prefer:
      “<drug>, intravenous infusion, <dose>”
    - Do NOT assume bolus vs infusion unless explicitly stated.

    4. Avoid Over-Specification
    - When multiple interpretations are possible, select the least specific
      term that remains billing-relevant.
    - Accuracy is preferred over granularity.
    """,

    # High-level description of the expected output
    expected_output="Structured output with ICD, CPT, HCPCS term lists",

    # Agent responsible for executing this task
    agent=Input_Structuring_Agent,

    # Enforces strict schema validation of the task output
    output_pydantic=Input_Structuring_Output_Model
)
