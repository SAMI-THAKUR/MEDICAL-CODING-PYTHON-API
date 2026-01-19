from app.core.tracing import langfuse

def add_evaluation_scores_to_langfuse(evaluation_result, trace_id):
    # Overall numeric score
    langfuse.create_score(
        trace_id=trace_id,
        name="overall_score",
        value=evaluation_result["overall_score"],
        data_type="NUMERIC",  # optional, possibly inferred
    )

    # Overall verdict (pass/fail)
    langfuse.create_score(
        trace_id=trace_id,
        name="overall_verdict",
        value=1 if evaluation_result["overall_verdict"].value == "pass" else 0,
        comment=evaluation_result.get("summary", ""),
        data_type="BOOLEAN"
    )

    # Compliance risk score
    langfuse.create_score(
        trace_id=trace_id,
        name="compliance_risk",
        value={
            "low": 1.0,
            "medium": 0.5,
            "high": 0.0,
        }.get(evaluation_result["compliance_risk"].value, 0.5),
        comment=f"Risk Level: {evaluation_result['compliance_risk'].value}",
        data_type="NUMERIC"
    )

    # Section-level scores
    for section_judge in evaluation_result["section_judgements"]:
        langfuse.create_score(
            trace_id=trace_id,
            name=f"section_{section_judge['section']}_verdict",
            value=1 if section_judge["verdict"].value == "pass" else 0,
            comment=section_judge.get("notes", ""),
            data_type="BOOLEAN"
        )

    # Code-level scores
    for code_judge in evaluation_result["code_judgements"]:
        code_name = f"code_{code_judge['code']}"
        code_type = code_judge["code_type"]

        # Documentation support score
        support_level = code_judge["documentation_support"].value
        support_score = {
            2: 1.0,  # FULLY_SUPPORTED
            1: 0.5,  # PARTIALLY_SUPPORTED
            0: 0.0,  # HALLUCINATED
        }.get(support_level, 0.0)

        langfuse.create_score(
            trace_id=trace_id,
            name=f"{code_name}_support",
            value=support_score,
            comment=(
                f"Term match: {code_judge['term_match']}, "
                f"Issues: {code_judge.get('issues', 'None')}"
            ),
            data_type="NUMERIC"
        )

        # Linkage validity (if applicable)
        if code_judge.get("linkage_valid") is not None:
            langfuse.create_score(
                trace_id=trace_id,
                name=f"{code_type}_{code_name}_linkage",
                value=1 if code_judge["linkage_valid"] else 0,
                comment="Linkage valid" if code_judge["linkage_valid"] else "Linkage invalid",
                data_type="BOOLEAN"
            )
