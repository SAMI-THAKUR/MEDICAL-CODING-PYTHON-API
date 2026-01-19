# 🏥 Medical Coding Pipeline API

A robust FastAPI backend for **automated medical billing code assignment** using CrewAI multi-agent architecture with RAG (Retrieval-Augmented Generation).

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Server](#-running-the-server)
- [API Documentation](#-api-documentation)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Team Members](#-team-members)

---

## ✨ Features

- **Multi-Agent System**: CrewAI-powered agents for ICD-10-CM, CPT-4, and HCPCS coding
- **RAG Pipeline**: Pinecone vector database + LLM reasoning for accurate code retrieval
- **LLM as Judge**: Quality evaluation and compliance checking
- **PDF Support**: Extract and process medical reports from PDFs with OCR fallback
- **Observability**: Full tracing with Langfuse for debugging and evaluation
- **RESTful API**: Clean API endpoints for integration with frontend applications

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FastAPI Backend                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Entity    │───▶│  ICD-10-CM  │───▶│   HCPCS     │         │
│  │ Structuring │    │   Coding    │    │   Coding    │         │
│  │   Agent     │    │   Agent     │    │   Agent     │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│         │                  │                  │                 │
│         │                  ▼                  ▼                 │
│         │           ┌─────────────┐    ┌─────────────┐         │
│         │           │  Pinecone   │    │   CPT-4     │         │
│         │           │  Vector DB  │    │   Coding    │         │
│         │           │    (RAG)    │    │   Agent     │         │
│         │           └─────────────┘    └─────────────┘         │
│         │                                     │                 │
│         └─────────────────────────────────────┘                 │
│                            │                                    │
│                            ▼                                    │
│                    ┌─────────────┐                              │
│                    │  LLM Judge  │                              │
│                    │ (Evaluation)│                              │
│                    └─────────────┘                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| **Python** | 3.11.x | `python --version` or `py --list` |
| **pip** | Latest | `pip --version` |
| **Git** | Latest | `git --version` |

### Windows Users
Make sure Python 3.11 is installed. You can check available Python versions with:
```bash
py --list
```

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Be-project/backend
```

### Step 2: Create Virtual Environment (Python 3.11)

**Windows (Command Prompt):**
```bash
py -3.11 -m venv venv
```

**Windows (PowerShell):**
```powershell
py -3.11 -m venv venv
```

**Linux/macOS:**
```bash
python3.11 -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Git Bash):**
```bash
source venv/Scripts/activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

> ✅ You should see `(venv)` in your terminal prompt after activation.

### Step 4: Verify Python Version

```bash
python --version
```
Expected output: `Python 3.11.x`

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

> ⏳ This may take a few minutes as it installs ML libraries like transformers, sentence-transformers, etc.

---

## ⚙️ Configuration

### Step 1: Create Environment File

Copy the example environment file:

**Windows:**
```bash
copy .env.example .env
```

**Linux/macOS:**
```bash
cp .env.example .env
```

### Step 2: Configure API Keys

Open `.env` in your editor and replace the placeholder values with your actual API keys:

```env
# LLM API Keys
GOOGLE_API_KEY=your_actual_google_api_key
GROQ_API_KEY=your_actual_groq_api_key
OPENROUTER_API_KEY=your_actual_openrouter_api_key

# Langfuse (Observability)
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key

# Pinecone (Vector Database)
PINECONE_API_KEY=your_pinecone_api_key
```

### Required API Keys

| Service | Purpose | Get Key From |
|---------|---------|--------------|
| **Google AI** | Gemini LLM | [Google AI Studio](https://aistudio.google.com/) |
| **Groq** | Fast LLM inference | [Groq Console](https://console.groq.com/) |
| **OpenRouter** | Multi-model access | [OpenRouter](https://openrouter.ai/) |
| **Langfuse** | Observability/Tracing | [Langfuse](https://langfuse.com/) |
| **Pinecone** | Vector Database | [Pinecone](https://www.pinecone.io/) |

> ⚠️ **Important**: Never commit your `.env` file to Git! It's already in `.gitignore`.

---

## 🖥️ Running the Server

### Development Mode (with auto-reload)

```bash
uvicorn app.main:app --reload
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Expected Output

```
🚀 Starting Medical Coding API v1.0.0
📍 Environment: development
🔗 API Docs: http://0.0.0.0:8000/docs
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

---

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

| Documentation | URL |
|---------------|-----|
| **Swagger UI** | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **ReDoc** | [http://localhost:8000/redoc](http://localhost:8000/redoc) |
| **OpenAPI JSON** | [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json) |

---

## � API Endpoints

### Health Check
```http
GET /api/v1/health
```
Returns service status and version.

### Process Medical Text
```http
POST /api/v1/coding/process
Content-Type: application/json

{
  "medical_report_text": "Patient: 67-year-old male. Assessment: Acute UTI...",
  "include_evaluation": true
}
```

### Process PDF Upload
```http
POST /api/v1/coding/process-pdf
Content-Type: multipart/form-data

file: <your-pdf-file>
include_evaluation: true
```

### Process Test PDF (Development Only)
```http
POST /api/v1/coding/process-test-pdf?filename=sample_medical_report.pdf
```
Place your test PDF in the `backend/` folder.

---

## �📁 Project Structure

```
backend/
├── 📄 .env.example          # Environment variables template
├── 📄 .gitignore            # Git ignore rules
├── 📄 README.md             # This file
├── 📄 requirements.txt      # Python dependencies
│
├── 📁 app/                  # Main application package
│   ├── 📄 __init__.py
│   ├── 📄 main.py           # FastAPI app entry point
│   │
│   ├── 📁 core/             # ⚙️ Configuration & Settings
│   │   ├── config.py            # Environment settings
│   │   ├── dependencies.py      # FastAPI DI
│   │   ├── llm_config.py        # LLM model configs
│   │   ├── vector_db.py         # Pinecone setup
│   │   └── observability.py     # Langfuse/OpenLIT
│   │
│   ├── 📁 models/           # 📋 Pydantic Schemas
│   │   ├── requests.py          # API request models
│   │   ├── responses.py         # API response models
│   │   ├── entities.py          # Medical entities
│   │   ├── icd_models.py        # ICD coding schemas
│   │   ├── cpt_models.py        # CPT coding schemas
│   │   ├── hcpcs_models.py      # HCPCS coding schemas
│   │   └── judge_models.py      # Evaluation schemas
│   │
│   ├── 📁 agents/           # 🤖 CrewAI Agents
│   │   ├── entity_structuring_agent.py
│   │   ├── icd_coding_agent.py
│   │   ├── cpt_coding_agent.py
│   │   ├── hcpcs_coding_agent.py
│   │   └── crew.py              # Crew orchestration
│   │
│   ├── 📁 tools/            # 🔧 RAG Vector Search Tools
│   │   ├── icd_search_tool.py
│   │   ├── cpt_search_tool.py
│   │   └── hcpcs_search_tool.py
│   │
│   ├── 📁 services/         # 💼 Business Logic
│   │   ├── pdf_extractor.py     # PDF text extraction
│   │   ├── coding_pipeline.py   # Main pipeline
│   │   ├── judge_service.py     # LLM as Judge
│   │   ├── embedding_service.py # Embeddings
│   │   └── tracing_service.py   # Langfuse tracing
│   │
│   ├── 📁 api/              # 🌐 API Routes
│   │   └── v1/
│   │       ├── router.py        # v1 router
│   │       └── endpoints/
│   │           ├── coding.py    # Coding endpoints
│   │           └── health.py    # Health check
│   │
│   └── 📁 utils/            # 🛠️ Utilities
│       ├── text_utils.py        # Text cleaning
│       ├── compression.py       # Response compression
│       └── exceptions.py        # Custom exceptions
│
└── 📁 tests/                # 🧪 Test Files
    ├── conftest.py              # Pytest fixtures
    ├── test_api.py              # API tests
    └── test_services.py         # Service tests
```

---

## 🧪 Testing

### Run Health Check

```bash
curl http://localhost:8000/api/v1/health
```

### Test with Sample Text (using curl)

```bash
curl -X POST "http://localhost:8000/api/v1/coding/process" \
  -H "Content-Type: application/json" \
  -d '{"medical_report_text": "Patient: 67-year-old male. Assessment: Acute UTI. Administered ciprofloxacin 400 mg IV.", "include_evaluation": false}'
```

### Test via Swagger UI

1. Open [http://localhost:8000/docs](http://localhost:8000/docs)
2. Click on the endpoint you want to test
3. Click "Try it out"
4. Enter your data and click "Execute"

---

## 🔧 Troubleshooting

### Common Issues

#### ❌ `ModuleNotFoundError: No module named 'app'`
**Solution**: Make sure you're in the `backend/` directory when running the server.

#### ❌ `Python 3.11 not found`
**Solution**: Install Python 3.11 from [python.org](https://www.python.org/downloads/)

#### ❌ `pip install fails`
**Solution**: Upgrade pip first:
```bash
python -m pip install --upgrade pip
```

#### ❌ `CORS errors from frontend`
**Solution**: Update `CORS_ORIGINS` in `.env` to include your frontend URL.

#### ❌ `Pinecone connection error`
**Solution**: Verify your `PINECONE_API_KEY` is correct and indexes exist.

### Getting Help

If you encounter issues:
1. Check the terminal logs for error messages
2. Verify all API keys in `.env` are correct
3. Ensure Pinecone indexes (`icd10`, `hcpcs`, `cpt`) are created and populated

---

## 👥 Team Members

| Name | Role | Contact |
|------|------|---------|
| [Your Name] | Lead Developer | [email] |
| [Team Member] | [Role] | [email] |

---

## 📄 License

This project is for educational purposes (BE Project - Semester 7).

---

## � Related Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Langfuse Documentation](https://langfuse.com/docs)

---

**Made with ❤️ for Medical Coding Automation**
