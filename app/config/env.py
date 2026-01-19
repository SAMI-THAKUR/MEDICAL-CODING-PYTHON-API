"""
Environment Variable Configuration
"""

# Imports for Pydantic Settings
from pydantic_settings import BaseSettings
from typing import List 


# Imports for Caching and Environment Variables
from functools import lru_cache
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


# Class for Environment Variables
class EnvironmentVariable(BaseSettings):
    """ Environment Variables loaded from .env file """
    # LLMs API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")

    # Langfuse API Keys
    LANGFUSE_PUBLIC_KEY: str = os.getenv("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_SECRET_KEY: str = os.getenv("LANGFUSE_SECRET_KEY")
    LANGFUSE_BASE_URL: str = os.getenv("LANGFUSE_BASE_URL")
    
    # Pinecone API Keys
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_ICD: str = os.getenv("PINECONE_INDEX_ICD")
    PINECONE_INDEX_HCPCS: str = os.getenv("PINECONE_INDEX_HCPCS")
    PINECONE_INDEX_CPT: str = os.getenv("PINECONE_INDEX_CPT")
    

# Function to get environment variables and cache them
@lru_cache
def get_env() -> EnvironmentVariable:
    """Cached environment variables"""
    return EnvironmentVariable()


env = get_env() # Global environment variables instance
