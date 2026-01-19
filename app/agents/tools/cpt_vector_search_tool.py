"""
CPT-4 Vector Search Tool
RAG tool for retrieving CPT-4 procedure codes from Pinecone
"""

# =========================
# Imports
# =========================
from typing import List
from crewai.tools import tool
from toon_format import encode
from app.core.tracing import langfuse
from app.core.vector_db import cpt_index
from app.core.embeddings import embedding_model
from app.agents.tools.helpers import compress_vector_db_response



# Load CPT vector database configuration once
vector_db = cpt_index


@tool
def CPT_Vector_Search_Tool(query_texts: List[str]) -> str:
    """
    Search the CPT-4 vector database for relevant medical procedure codes.

    Args:
        query_texts (List[str]):
            List of procedure or service terms to search for.

    Returns:
        str:
            Human-readable formatted search results for each term.
    """

    # Start a Langfuse tracing span for this tool execution
    with langfuse.start_as_current_span(
        name="CPT Vector Search Tool",
    ) as span:

        # Collect results for all procedure queries
        queries_results = []

        # Process each query independently
        for query_text in query_texts:

            # Defensive validation: input must be text
            if not isinstance(query_text, str):
                raise ValueError(
                    "CPT vector search accepts a list of strings only."
                )

            # 1. Generate embedding for the procedure term
            embedding = embedding_model.encode(query_text)
            if hasattr(embedding, "tolist"):
                embedding = embedding.tolist()

            # 2. Query the Pinecone CPT index using vector similarity
            results = vector_db.query(
                vector=embedding,
                top_k=5,
                include_metadata=True,
            )

            # 3. Compress Pinecone response to reduce token usage
            results = compress_vector_db_response(results)

            # 4. Encode results into the final tool output format
            results = encode(results)

            # 5. Append formatted output for this query
            queries_results.append(
                f"Results for procedure term '{query_text}':\n{results}"
            )

        # Attach structured input/output data to the Langfuse trace
        span.update(
            input=query_texts,
            output=queries_results,
            metadata={"index": "CPT"},
        )

        # Return combined results for all queries
        return "\n\n".join(queries_results)
