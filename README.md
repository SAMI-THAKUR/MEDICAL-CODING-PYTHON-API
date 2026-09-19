# MEDICAL CODING BACKEND

A FastAPI-based medical coding backend that processes clinical notes using a multi-agent CrewAI pipeline to extract structured entities and assign coding candidates across ICD-10-CM, CPT-4, and HCPCS Level II.

## Overview

This project transforms raw medical report text into structured, coding-ready outputs by combining:

- FastAPI APIs
- CrewAI multi-agent orchestration
- Vector-based retrieval for coding reference data
- LLM-powered reasoning and evaluation
- Langfuse observability and trace tracking

The backend is designed to support medical coding workflows such as:

- Extracting diagnoses, medications, procedures, and findings
- Mapping relevant entities to ICD-10-CM codes
- Mapping procedures to CPT-4 codes
- Mapping medications / supplies / services to HCPCS Level II codes
- Returning structured outputs for downstream review or UI integration

---

## Features

- Multi-agent architecture for medical entity extraction and coding
- Structured API input/output models
- REST API built with FastAPI
- CrewAI-based orchestration for coding agents
- Vector database support for retrieval-augmented coding assistance
- Langfuse tracing for execution monitoring and debugging
- LLM-as-Judge evaluation support
- CORS-enabled backend for frontend integration

---

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic / Pydantic Settings
- CrewAI
- LangChain / Google GenAI
- Pinecone
- Langfuse
- Sentence Transformers
- Python-dotenv

---

## Project Structure

```text
backend/
├── app/
│   ├── agents/
│   │   ├── input_structuring_agent.py
│   │   ├── icd_coding_agent.py
│   │   ├── cpt_coding_agent.py
│   │   ├── hcpcs_coding_agent.py
│   │   ├── crew.py
│   │   └── tools/
│   │       ├── icd_vector_search_tool.py
│   │       ├── cpt_vector_search_tool.py
│   │       ├── hcpcs_vector_search_tool.py
│   │       └── helpers.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── health.py
│   │           └── coding.py
│   │
│   ├── config/
│   │   ├── env.py
│   │   └── settings.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── embeddings.py
│   │   ├── llm_config.py
│   │   ├── tracing.py
│   │   └── vector_db.py
│   │
│   ├── evaluation/
│   │   ├── judge.py
│   │   └── metrics.py
│   │
│   ├── models/
│   │   ├── requests.py
│   │   ├── responses.py
│   │   ├── input_structuring_models.py
│   │   ├── icd_models.py
│   │   ├── cpt_models.py
│   │   ├── hcpcs_models.py
│   │   └── judge_models.py
│   │
│   ├── services/
│   │   ├── medical_coding_pipeline.py
│   │   ├── llm_as_judge.py
│   │   └── pdf_extractor.py
│   │
│   ├── tasks/
│   │   ├── input_structuring_task.py
│   │   ├── icd_coding_task.py
│   │   ├── cpt_coding_task.py
│   │   └── hcpcs_coding_task.py
│   │
│   ├── main.py
│   └── medical_coding_crew.py
│
├── requirements.txt
├── Dockerfile
├── README.md
├── README-Agents.md
└── sample_medical_report_1.pdf

The backend follows a pipeline-based design:

1. Input medical text is received from the API
2. The input structuring agent extracts clinically relevant entities
3. Diagnosis, procedure, and supply coding agents process the structured entities
4. Retrieval and LLM reasoning are used to select candidate codes
5. Output is aggregated and returned in JSON
6. Optional evaluator runs a quality review using LLM-as-Judge
7. Langfuse captures input, output, and trace metadata

```text
Medical Report Text
        |
        v
Input Structuring Agent
        |
        v
ICD / CPT / HCPCS Coding Agents
        |
        v
Vector Search + LLM Reasoning
        |
        v
Structured Coding Output
        |
        v
LLM Judge / Evaluation
        |
        v
FastAPI Response
```

---

## Environment Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

On Windows:
```bash
.venv\Scripts\activate
```

On macOS/Linux:
```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project environment and configure the required values.

Example:

```env
APP_NAME=Medical Coding API
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8001

GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_BASE_URL=https://cloud.langfuse.com

PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_ICD=icd10
PINECONE_INDEX_HCPCS=hcpcs
PINECONE_INDEX_CPT=cpt

CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

> Keep your `.env` file private and do not commit secrets to version control.

---

## Running the Server

From the backend root:

```bash
uvicorn app.main:app --reload
```

Or with explicit host and port:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

The app will start with FastAPI docs available at:

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

---

## API Endpoints

### Health check

```http
GET /api/v1/health
```

Example response:

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

### Process medical report text

```http
POST /api/v1/coding/process/text
```

Request body:

```json
{
  "medical_report_text": "Patient is a 67-year-old male with chronic cough, wheezing, and shortness of breath. Diagnosed with acute bronchitis. Prescribed albuterol inhaler and ordered chest X-ray.",
  "include_evaluation": true
}
```

Example response structure:

```json
{
  "extracted_entities": {
    "diagnoses": [],
    "medications": [],
    "procedures": [],
    "findings": []
  },
  "icd_codes": {
    "icd_codes": []
  },
  "cpt_codes": {
    "cpt_codes": []
  },
  "hcpcs_codes": {
    "hcpcs_codes": []
  },
  "evaluation": {},
  "trace_id": "..."
}
```

---

## Request and Response Models

The backend uses Pydantic models for validation.

### ProcessTextRequest

```python
class ProcessTextRequest(BaseModel):
    medical_report_text: str
    include_evaluation: bool = True
```

### HealthResponse

```python
class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
```

## Coding Workflow

The system is designed around a clinical coding pipeline:

- Input structuring agent identifies medically relevant entities
- Each coding agent maps extracted data into relevant code families
- Vector retrieval is used to search code repositories or indexing stores
- LLMs weigh clinical context and retrieve best-fit candidates
- Final output is merged into a unified response
- Evaluation can be included for quality checks

---

## Notes on Observability

The project uses Langfuse for tracing, enabling:

- End-to-end request tracking
- Prompt and output visibility
- Trace IDs for debugging
- Metadata collection for auditability

Each pipeline execution generates a `trace_id` that is returned with the output.

---

## Development Notes

- The application entry point is `app/main.py`
- The API router is configured in `app/api/v1/router.py`
- The orchestration logic is in `app/medical_coding_crew.py`
- The coding pipeline lives in `app/services/medical_coding_pipeline.py`
- Environment settings are defined in `app/config/settings.py` and `app/core/config.py`

---

## Troubleshooting

### Server fails to start
Check that dependencies are installed and that your virtual environment is active:

```bash
pip install -r requirements.txt
```

### Missing API keys
Ensure your `.env` file contains valid values for the services you use:

- `GOOGLE_API_KEY`
- `GROQ_API_KEY`
- `OPENROUTER_API_KEY`
- `PINECONE_API_KEY`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`

### CORS issues
Update `CORS_ORIGINS` in the environment or config to include your frontend origin.

### No outputs from coding pipeline
Confirm that the model providers and vector search configuration are valid and that your vector indexes exist.

---

## License

This project is intended for internal or research use unless otherwise stated by the repository owner.

---

## Summary

This backend provides a practical foundation for medical coding automation using AI-driven, multi-agent reasoning. It is suited for experimentation, API integration, and deployment into clinical documentation or coding review workflows.
