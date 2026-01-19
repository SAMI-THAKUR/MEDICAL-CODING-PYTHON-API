"""
ICD-10 Vector Search Tool
RAG tool for retrieving ICD-10-CM codes from Pinecone
"""

# =========================
# Imports
# =========================
from typing import List 
from crewai.tools import tool
from toon_format import encode
from app.core.tracing import langfuse
from app.core.vector_db import icd_index
from app.core.embeddings import embedding_model
from app.agents.tools.helpers import compress_icd_10_vector_db_response


# Get the ICD vector database configuration once at import time
vector_db = icd_index

@tool
def ICD_Vector_Search_Tool(query_texts: List[str]) -> str:
    """
    Search the ICD-10 vector database for relevant diagnostic codes.

    Args:
        query_texts (List[str]):
            List of diagnostic terms (free text) to search for.

    Returns:
        str:
            Human-readable formatted search results for each term.
    """

    # Start a Langfuse tracing span for this tool execution
    with langfuse.start_as_current_span(
        name="ICD Vector Search Tool",
    ) as span:

        # Collect results for all queries
        queries_results = []

        # Process each diagnostic term independently
        for query_text in query_texts:

            # Defensive check: tool expects text inputs only
            if not isinstance(query_text, str):
                raise ValueError(
                    "ICD vector search accepts a list of strings only."
                )

            # 1. Generate embedding for the diagnostic term
            embedding = embedding_model.encode(query_text)
            if hasattr(embedding, "tolist"):
                embedding = embedding.tolist()

            # 2. Query Pinecone ICD-10 index using vector similarity
            results = vector_db.query(
                vector=embedding,
                top_k=5,
                include_metadata=True,
            )

            # 3. Compress Pinecone response to reduce token usage
            results = compress_icd_10_vector_db_response(results)

            # 4. Encode results into the final tool output format
            results = encode(results)

            # 5. Store formatted results for this query
            queries_results.append(
                f"Results for diagnostic term '{query_text}':\n{results}"
            )

        # Attach structured input/output data to the trace
        span.update(
            input=query_texts,
            output=queries_results,
            metadata={"index": "ICD-10-CM"},
        )

        # Return a single string containing all query results
        return "\n\n".join(queries_results)
