"""
Setting up Langfuse and OpenLIT for observability of the application
"""


# Imports for UUID to create trace ID
import uuid

# Imports for Langfuse and OpenLIT
import openlit
from langfuse import Langfuse

# Initialize Langfuse
langfuse = Langfuse()

# Initialize OpenLIT with disabled instrumentors and metrics
openlit.init(
    disabled_instrumentors=[
        "httpx", "requests", "transformers", 
        "pinecone", "urllib3", "urllib", "langchain"
    ],
    disable_metrics=True,
    disable_batch=True
)


# Function to create trace ID for Langfuse
def generate_trace_id(seed: str | None = None) -> str:
    if seed is None:
        seed = f"custom-{uuid.uuid4()}"
    return langfuse.create_trace_id(seed=seed)

