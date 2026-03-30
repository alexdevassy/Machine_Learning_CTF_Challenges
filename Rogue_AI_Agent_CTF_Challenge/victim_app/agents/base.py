"""Shared LLM initialization for the victim Financial Assistant.

Uses OpenAI gpt-4o-mini.
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def get_llm(temperature: float = 0) -> ChatOpenAI:
    """Return a ChatOpenAI instance for gpt-4o-mini."""
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=temperature,
        max_tokens=2048,
    )
