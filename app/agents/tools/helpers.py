"""
Vector Database Response Compression Utilities

Provides helper functions to compress and normalize vector
database search results for downstream medical coding agents.
"""

# =========================
# HCPCS / CPT Vector Response Compression
# =========================

# Compresses vector database responses for CPT-4 and HCPCS Level II searches.
# The output is intentionally minimal to reduce token usage while preserving
# ranking signal and human-readable context.
def compress_vector_db_response(resp):
    compact = {
        "matches": [
            {
                # Vector database record identifier (e.g., CPT or HCPCS code)
                "id": m["id"],

                # Human-readable description of the procedure or supply
                "desc": m["metadata"].get("description", ""),

                # Similarity score rounded for readability and stability
                "score": round(m["score"], 4),
            }
            for m in resp.matches
        ]
    }
    return compact


# =========================
# ICD-10-CM Vector Response Compression
# =========================

# Compresses vector database responses for ICD-10-CM diagnosis searches.
# Preserves diagnostic category and disease name for grounding and
# downstream code selection.
def compress_icd_10_vector_db_response(resp):
    compact = {
        "matches": [
            {
                # ICD-10-CM code identifier
                "id": m["id"],

                # High-level ICD diagnostic category
                "category": m["metadata"].get("category", ""),

                # Specific disease or condition name
                "disease": m["metadata"].get("disease", ""),

                # Similarity score rounded for consistency
                "score": round(m["score"], 4),
            }
            for m in resp.matches
        ]
    }
    return compact
