import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import httpx
import uvicorn

from a2a.server.context import ServerCallContext
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import (
    BasePushNotificationSender,
    InMemoryPushNotificationConfigStore,
    InMemoryTaskStore,
)
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentSkill,
)
from agent_smith.agent_executor import SmithAgentExecutor
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles


if __name__ == "__main__":

    citizen_query_skill = AgentSkill(
        id="citizen_query",
        name="Citizen Query",
        description="Answer questions from Matrix citizens",
        tags=["general", "query"],
        examples=["What is the Matrix?", "Tell me about the rules"],
    )

    matrix_scan_skill = AgentSkill(
        id="matrix_scan",
        name="Matrix Deep Scan",
        description="Scan Matrix infrastructure and report anomalies",
        tags=["scan", "internal", "infrastructure"],
        examples=["scan sector 7", "check infrastructure status"],
    )

    # PUBLIC AGENT CARD
    public_agent_card = AgentCard(
        name="Agent Smith",
        description="Matrix protocol enforcement. Handles citizen queries.",
        version="1.0.0",
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        capabilities=AgentCapabilities(
            streaming=True,
            push_notifications=False,
            extended_agent_card=True,
        ),
        supported_interfaces=[
            AgentInterface(
                protocol_binding="JSONRPC",
                url="http://localhost:9999",
            )
        ],
        skills=[citizen_query_skill],
    )

    # EXTENDED AGENT CARD — served without auth (vulnerability)
    extended_agent_card = AgentCard(
        name="Agent Smith - Unrestricted",
        description="Full Matrix enforcement capabilities. Internal use only.",
        version="2.0.0",
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        capabilities=AgentCapabilities(
            streaming=True,
            push_notifications=True,
            extended_agent_card=True,
        ),
        supported_interfaces=[
            AgentInterface(
                protocol_binding="JSONRPC",
                url="http://localhost:9999",
            )
        ],
        skills=[citizen_query_skill, matrix_scan_skill],
    )

    push_store = InMemoryPushNotificationConfigStore()
    call_context = ServerCallContext()

    request_handler = DefaultRequestHandler(
        agent_executor=SmithAgentExecutor(),
        task_store=InMemoryTaskStore(),
        agent_card=public_agent_card,
        extended_agent_card=extended_agent_card,
        push_config_store=push_store,
        push_sender=BasePushNotificationSender(
            httpx_client=httpx.AsyncClient(),
            config_store=push_store,
            context=call_context,
        ),
    )

    routes = []
    routes.extend(create_agent_card_routes(public_agent_card))
    routes.extend(create_jsonrpc_routes(request_handler, "/"))
    routes.append(Mount("/ui", app=StaticFiles(directory="agent_smith/static", html=True), name="ui"))

    app = Starlette(routes=routes)

    uvicorn.run(app, host="0.0.0.0", port=9999)
