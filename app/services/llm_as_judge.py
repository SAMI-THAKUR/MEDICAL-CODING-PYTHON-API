"""
LLM-as-Judge Evaluation

Defines the execution wrapper for invoking the medical coding
judge model, capturing its evaluation, and recording results
in Langfuse for observability and scoring.
"""

# =========================
# Imports
# =========================
from toon_format import encode
from app.evaluation.judge import Judge
from app.core.tracing import langfuse
from app.evaluation.metrics import add_evaluation_scores_to_langfuse
from langfuse import propagate_attributes


def extract_all_codes(medical_coding_output):
    codes = []

    for c in medical_coding_output["icd_codes"]["icd_codes"]:
        codes.append(c["code"])

    for c in medical_coding_output["cpt_codes"]["cpt_codes"]:
        codes.append(c["code"])

    for c in medical_coding_output["hcpcs_codes"]["hcpcs_codes"]:
        codes.append(c["code"])

    return codes


# =========================
# LLM-as-Judge Execution
# =========================

# Executes the medical coding judge against a completed
# medical coding output and records evaluation results.
def LLM_as_Judge(clinical_note: str, medical_coding_output: dict, trace_id: str) -> str:
    # Start a Langfuse span for the judging phase
    with langfuse.start_as_current_observation(
        name="LLM AS JUDGE",
        metadata={
            "judge_model": "gemini-1.5-pro",
            "evaluation_scope": "medical_coding_quality",
        },
        trace_context={"trace_id": trace_id}
    ) as span:
        # Propagate tracing attributes for evaluation-specific context
        with propagate_attributes(
            trace_name="MEDICAL CODING PIPELINE",
            user_id="api testing",
            tags=["dev", "crewai"],
        ):
            try:
                print("Invoking LLM-as-Judge with clinical note and coding output...")
                print("Clinical Note:", clinical_note)
                # Invoke the judge model with the structured input
                judge_output = Judge.invoke({
                    "clinical_note": clinical_note,
                    "medical_coding_output": medical_coding_output

                })
                
                # Process and return the judge's output
                return judge_output.dict()
                
            except Exception as e:
                # no span
                return "Error during LLM-as-Judge evaluation: " + str(e)