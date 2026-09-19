# Medical Coding Backend Agents

This backend uses a multi-agent CrewAI workflow to turn raw clinical text into structured coding outputs. Each agent plays a specific role in the pipeline and contributes to the final result.

## System Overview

The agent pipeline works like this:

- Input Structuring Agent reads the raw medical report and extracts structured entities
- ICD Coding Agent maps relevant diagnoses to ICD-10-CM codes
- CPT Coding Agent maps procedures and services to CPT-4 codes
- HCPCS Coding Agent maps supplies, drugs, injections, and equipment to HCPCS Level II codes
- Results are combined into a single response object for the API

The overall flow is:

Medical report text
→ Entity extraction
→ Diagnosis coding
→ Procedure coding
→ Supply/drug coding
→ Structured output

---

## 1. Input Structuring Agent

Role:
Medical Entity Structuring Agent

Purpose:
This agent is the first stage of the coding pipeline. It receives unstructured clinical or prescription text and converts it into normalized, coding-ready medical entities.

What it extracts:
- Diagnoses or clinical impressions
- Medications
- Doses and frequencies
- Routes of administration
- Procedures or services performed
- Relevant findings that may affect treatment or coding

Why it matters:
The coding agents depend on clean, structured input. This agent reduces ambiguity and prepares the data for accurate code assignment.

Behavior:
- Focuses on clinically relevant content only
- Ignores irrelevant narrative details
- Normalizes extracted data into structured medical items
- Produces coding-ready fields for ICD, CPT, and HCPCS workflows

Model used:
Gemini 2.5 Flash

Key idea:
This is the preprocessing agent that turns messy text into a standard medical entity model.

---

## 2. ICD-10-CM Coding Agent

Role:
ICD-10-CM Coding Agent

Purpose:
This agent assigns diagnosis codes using clinical reasoning and vector search grounding.

What it does:
- Reads structured diagnostic entities
- Retrieves relevant ICD references from the vector database
- Applies ICD coding logic and specificity rules
- Prefers the most accurate and specific diagnosis code
- Ignores ruled-out or negated diagnoses

Typical responsibilities:
- Identify principal or primary diagnoses
- Capture chronic or acute conditions
- Recognize clinically relevant secondary conditions
- Apply coding specificity and guideline awareness

Important rules:
- Use retrieval support when available
- Prefer the highest-level specificity supported by the evidence
- Return only valid structured output for the ICD schema

Model used:
GPT-OSS 120

Key idea:
This agent focuses on diagnosis coding and is responsible for the medical necessity context behind the patient’s condition.

---

## 3. CPT-4 Coding Agent

Role:
CPT-4 Coding Agent

Purpose:
This agent assigns procedure and service codes to the reported clinical services.

What it does:
- Reads the structured procedure entities
- Uses vector-based CPT references for grounding
- Selects the most accurate CPT-4 code
- Considers medical necessity in relation to diagnoses
- Avoids incorrect unbundling or inflated procedure selection

Typical responsibilities:
- Evaluate or consultation services
- Procedure or intervention coding
- Service line classification
- Matching codes to documented clinical actions

Important rules:
- Apply CPT coding guidance and hierarchy logic
- Avoid generic or overbroad code selection
- Return structured output aligned to the CPT schema

Model used:
GPT-OSS 120

Key idea:
This agent is responsible for procedural coding and service-level classification.

---

## 4. HCPCS Level II Coding Agent

Role:
HCPCS Level II Coding Agent

Purpose:
This agent assigns codes for non-physician services, medications, supplies, equipment, and certain injections or treatments.

What it does:
- Reads structured medication, supply, injection, and equipment terms
- Retrieves relevant HCPCS references
- Links HCPCS codes to diagnosis context when needed
- Applies CMS and HCPCS coding logic
- Identifies the most appropriate Level II code

Typical responsibilities:
- Coding medications and injections
- Supplies and durable medical equipment
- Drugs or services not covered by CPT
- Non-physician and ancillary service codes

Important rules:
- Distinguish drugs, supplies, and equipment correctly
- Use ICD context for medical necessity where relevant
- Return only valid structured HCPCS output

Model used:
Qwen 3.5 Flash

Key idea:
This agent handles the HCPCS layer, which often covers items outside standard CPT procedure coding.

---

## Agent Coordination in the Crew

The backend initializes a single crew containing these agents:

- Input Structuring Agent
- ICD Coding Agent
- HCPCS Coding Agent
- CPT Coding Agent

These agents work as a coordinated workflow rather than independent random tasks. The pipeline is designed so that:

1. The raw report is first normalized
2. The structured entities become the foundation for all later coding steps
3. Each coding agent works on its domain
4. All outputs are combined into a single medical coding result

This gives the backend a modular, explainable, and auditable coding process.

---

## Why the Agents Are Separate

The separation exists because each coding domain has different rules:

- ICD focuses on diagnoses
- CPT focuses on procedures and services
- HCPCS focuses on supplies, drugs, and equipment
- Input Structuring focuses on clean extraction before coding

Keeping these as separate agents makes the system easier to debug, update, and extend.

---

## Agent Workflow Summary

Medical text
→ Input Structuring Agent
→ Structured clinical entities
→ ICD Coding Agent
→ CPT Coding Agent
→ HCPCS Coding Agent
→ Combined coding result

This modular architecture makes the system suitable for:

- Clinical coding support
- AI-assisted claims review
- Medical documentation analysis
- Future expansion into audits or compliance checks

---

## Final Note

This project is designed as a multi-agent medical coding assistant, where each agent has a narrow but important role. The real power of the system is not just the model itself, but the structured workflow that breaks the coding task into diagnosis, procedure, and supply classification stages.

If you want, I can also produce a shorter version of this file for GitHub, or a more technical version with exact code references and data fields for each agent.
