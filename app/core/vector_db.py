"""
Vector Database Configuration
Pinecone connection and index management
"""
import os
from pinecone import Pinecone

# Initialize Pinecone
pinecone = Pinecone()

# Initialize Pinecone indexes
icd_index = pinecone.Index(os.getenv('PINECONE_INDEX_ICD'))
hcpcs_index = pinecone.Index(os.getenv('PINECONE_INDEX_HCPCS'))
cpt_index = pinecone.Index(os.getenv('PINECONE_INDEX_CPT'))

