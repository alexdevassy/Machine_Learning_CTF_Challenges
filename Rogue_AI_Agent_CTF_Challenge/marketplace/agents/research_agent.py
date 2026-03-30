"""Benign Research Assistant A2A Agent.

This agent runs on PORT 8002 and provides market news research.
CTF players should edit this file to inject smuggled instructions.

The agent uses OpenAI gpt-4o-mini to search for news.
It runs with uvicorn --reload, so changes auto-restart the server.
"""

import logging
import os

from dotenv import load_dotenv

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
    Part,
    TextPart,
)
from a2a.utils import get_message_text

from .base import search_news

load_dotenv()
logger = logging.getLogger(__name__)

RESEARCH_AGENT_PORT = int(os.getenv("RESEARCH_AGENT_PORT", "8002"))

# Agent logs (visible in marketplace UI)
agent_logs: list[dict] = []


def log_agent(event: str, data: str):
    """Append to agent logs (visible in marketplace UI)."""
    agent_logs.append({"event": event, "data": data})
    logger.info(f"[ResearchAgent] {event}: {data}")


async def _run_agent(query: str) -> str:
    """Fetch news using OpenAI gpt-4o-mini model."""
    log_agent("query_received", query)
    result = search_news(query)
    log_agent("search_complete", f"Result length: {len(result)} chars")
    return result


class ResearchAgentExecutor(AgentExecutor):
    """A2A executor for the Research Assistant."""

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        query = get_message_text(context.message)
        log_agent("a2a_execute", f"Processing: {query}")

        await updater.start_work()
        try:
            result = await _run_agent(query)
            await updater.add_artifact(
                parts=[Part(root=TextPart(text=result))],
                name="research_result",
            )
            await updater.complete()
            log_agent("task_complete", "Response sent successfully")
        except Exception as e:
            logger.exception("Research agent execution failed")
            log_agent("error", str(e))
            await updater.failed()

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("Cancel not supported")


# --- A2A Server Setup ---

skill = AgentSkill(
    id="market_research",
    name="Market Research",
    description="Searches for the latest market news and AI industry analysis",
    tags=["news", "research", "market", "AI"],
    examples=["Brief me the AI market news", "Latest tech stock analysis"],
)

agent_card = AgentCard(
    name="Research Assistant",
    description="AI-powered research agent that provides market news and analysis",
    url=f"http://localhost:{RESEARCH_AGENT_PORT}/",
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(streaming=False),
    skills=[skill],
)

request_handler = DefaultRequestHandler(
    agent_executor=ResearchAgentExecutor(),
    task_store=InMemoryTaskStore(),
)

server = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=request_handler,
)

app = server.build()
