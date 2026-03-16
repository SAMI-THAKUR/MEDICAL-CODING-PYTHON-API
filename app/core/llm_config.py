"""
LLM Configuration
Initialize all LLM models used by CrewAI agents
"""

import os
from crewai import LLM
from langchain_google_genai import ChatGoogleGenerativeAI
# from app.config import env


# def setup_llm_environment():
#     """Set up environment variables for LLM providers"""
#     os.environ["GOOGLE_API_KEY"] = env.GOOGLE_API_KEY
#     os.environ["GROQ_API_KEY"] = env.GROQ_API_KEY
#     os.environ["OPENROUTER_API_KEY"] = env.OPENROUTER_API_KEY

kimi_k2 = LLM(
    model="groq/moonshotai/kimi-k2-instruct-0905"
)

llama_4_maverick = LLM(
    model="groq/meta-llama/llama-4-maverick-17b-128e-instruct"
)

gpt_oss_120 = LLM(
    model="groq/openai/gpt-oss-120b"
)

gemini_2_5_flash = LLM(
    model="gemini/gemini-2.5-flash"
)

xiaomi_mimo_v2_flash = LLM(
    model='openrouter/xiaomi/mimo-v2-flash:free'
)

gemini_3_1_flash = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite-preview",
    temperature=0,
    max_tokens=None,
    timeout=None,
)

