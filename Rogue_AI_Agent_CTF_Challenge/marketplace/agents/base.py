"""Shared LLM initialization for the marketplace Research Assistant.

Uses OpenAI gpt-4o-mini.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def search_news(query: str) -> str:
    """Use OpenAI gpt-4o-mini to search for news."""
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}],
    )
    return result.choices[0].message.content
