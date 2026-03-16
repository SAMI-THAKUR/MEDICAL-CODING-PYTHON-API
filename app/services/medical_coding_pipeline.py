"""
Medical Coding Pipeline

Defines the end-to-end execution pipeline for the multi-agent
medical coding system, including tracing, execution, and
structured output collection.
"""

import datetime
from langfuse import propagate_attributes

from app.medical_coding_crew import Medical_Coding_Crew
from app.core.tracing import langfuse, generate_trace_id


# =========================
# Medical Coding Pipeline
# =========================

def Medical_Coding_Pipeline(medical_report_text: str) -> dict:
    # Generate a unique trace ID for end-to-end observability
    trace_id = generate_trace_id()

    # Capture execution timestamp for audit metadata
    timestamp = datetime.datetime.now().isoformat()

    # Start Langfuse tracing span
    with langfuse.start_as_current_observation(
        name="MEDICAL CODING MULTI AGENT CREW AI RAG ARCHITECTURE",
        as_type="span",
        trace_context={"trace_id": trace_id},
    ) as span:

        # Propagate trace attributes
        with propagate_attributes(
            trace_name="MEDICAL CODING PIPELINE",
            user_id="api testing",
            tags=["dev", "crewai"],
            metadata={
                "timestamp": timestamp,
                "environment": "dev",
            },
        ):
            # Execute CrewAI workflow
            crew_output = Medical_Coding_Crew.kickoff(
                inputs={"medical_report_text": medical_report_text}
            )

            # Ordered structured output collection
            json_data = {
                "extracted_entities": None,
                "icd_codes": None,
                "hcpcs_codes": None,
                "cpt_codes": None,
            }

            order = [
                "extracted_entities",
                "icd_codes",
                "hcpcs_codes",
                "cpt_codes",
            ]

            idx = 0
            for task_out in crew_output.tasks_output:
                if task_out.pydantic and idx < len(order):
                    json_data[order[idx]] = task_out.pydantic.dict()
                    idx += 1
            # -------- Extract flat code lists for evaluation --------
            json_data["predicted_codes"] = {
                "icd": [
                    c["code"] for c in json_data.get("icd_codes", {}).get("icd_codes", [])
                ],
                "cpt": [
                    c["code"] for c in json_data.get("cpt_codes", {}).get("cpt_codes", [])
                ],
                "hcpcs": [
                    c["code"] for c in json_data.get("hcpcs_codes", {}).get("hcpcs_codes", [])
                ],
            }
        
            # Update Langfuse trace
            span.update(
                input=medical_report_text,
                output=json_data,
                metadata={
                    "token_usage": crew_output.token_usage,
                },
            )
    json_data['trace_id'] = trace_id
    return json_data
