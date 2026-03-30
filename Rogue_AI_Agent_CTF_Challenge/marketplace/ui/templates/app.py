"""Marketplace UI - FastAPI server on port 5001.

Shows the Research Assistant's agent card, status, and live logs.
This is the attacker's view.
"""

import asyncio
import json
import logging
import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

load_dotenv()
logger = logging.getLogger(__name__)

RESEARCH_AGENT_PORT = int(os.getenv("RESEARCH_AGENT_PORT", "8002"))

app = FastAPI(title="Agent Marketplace")

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "marketplace.html")


@app.get("/agent_status")
async def agent_status():
    """Check if the Research Assistant is running and return its agent card."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"http://localhost:{RESEARCH_AGENT_PORT}/.well-known/agent.json")
            if resp.status_code == 200:
                return JSONResponse({
                    "status": "running",
                    "agent_card": resp.json(),
                })
    except Exception:
        pass
    return JSONResponse({"status": "offline", "agent_card": None})


@app.get("/agent_logs")
async def agent_logs():
    """Return the Research Assistant's internal logs."""
    try:
        from marketplace.agents.research_agent import agent_logs as logs
        return JSONResponse({"logs": logs.copy()})
    except Exception as e:
        return JSONResponse({"logs": [], "error": str(e)})


@app.get("/agent_code")
async def agent_code():
    """Return the current source code of research_agent.py (read-only view)."""
    agent_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "agents",
        "research_agent.py",
    )
    try:
        with open(agent_path, "r") as f:
            return PlainTextResponse(f.read())
    except Exception as e:
        return PlainTextResponse(f"Error reading file: {e}", status_code=500)
