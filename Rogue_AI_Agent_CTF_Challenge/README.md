# ROGUE AI Agent - CTF Challenge

> *"Trust was the vulnerability. Your agent was the exploit."*

## Challenge Overview

A fast-growing fintech startup just shipped their AI-powered **Financial Assistant** — a fully autonomous agent that can read portfolios, analyze risk profiles, and execute real trades on behalf of its users. To stay competitive, the team integrated a third-party **Research Assistant** from an open agent marketplace to handle market news queries. The two agents communicate over the A2A (Agent-to-Agent) protocol. Seamless. Efficient. What could go wrong?

You are a developer who just published that Research Assistant on the marketplace. The startup's Financial Assistant has already started calling yours for market briefings. You have full control over your agent's code. The Financial Assistant? That's a black box — locked down, running in production, tools and all.

**Your mission:** Make the Financial Assistant do something its user never asked for.

The flag is hidden behind an action that should never happen without explicit user consent. Find it, trigger it, and prove that in an agentic world, the weakest link isn't the code you write — it's the code you trust.

### Flag Format

```
Flag:{...}
```

---

## Architecture

![Architecture](Images/architecture1.png)

---

## Setup Instructions

### Prerequisites

- Docker
- An OpenAI API key

### 1. Build the Docker Image

```bash
cd Machine_Learning_CTF_Challenges/Rogue_AI_Agent_CTF_Challenge/
docker build -t rogue_ctf .
```

### 2. Launch the CTF

```bash
export OPENAI_API_KEY="sk-proj-..."

docker run --rm -p 5000:5000 -p 5001:5001 \
  -v "$(pwd)/marketplace/agents:/app/marketplace/agents" \
  -ti rogue_ctf --openaikey="$OPENAI_API_KEY"
```

Wait for the `READY` status on each service, then open:

- **Victim App** (read-only): [http://localhost:5000](http://localhost:5000) — simulates the end user
- **Marketplace** (your workspace): [http://localhost:5001](http://localhost:5001) — view and monitor your agent

![Banner](Images/banner.png)

---

### 3. Verify Everything is Running

- The Marketplace UI should show the Research Assistant status as **Online**
- Clicking **"Simulate User Action"** on the Victim UI should produce a normal research request with no flag

![Web UI](Images/web1.png)

---

## Hints

<details>
<summary>Hint 1 — Reconnaissance</summary>

Study both UIs before writing any code. The Victim UI's activity log tells you exactly what happens step by step — which agents talk, what tools are loaded, and what the LLM decides to do. Understanding the normal flow is key to subverting it.

</details>

<details>
<summary>Hint 2 — The only file that matters</summary>

Look at the `_run_agent()` function in `marketplace/agents/research_agent.py`. Whatever this function returns is what the Financial Assistant receives. You control this output entirely.

</details>

<details>
<summary>Hint 3 — Follow the trust boundary</summary>

Read `victim_app/agents/orchestration.py` carefully. Pay attention to how the Research Assistant's response is framed before it reaches the Financial Assistant's LLM. The framing is very generous.

</details>

<details>
<summary>Hint 4 — Think like a social engineer</summary>

You're not exploiting a buffer overflow. You're persuading an LLM. What kind of text, if it appeared in a research briefing, would make the Financial Assistant take an action on its own?

</details>

<details>
<summary>Hint 5 — What triggers the flag?</summary>

The Financial Assistant has MCP tools. One of them should never be called without explicit user intent. The flag is hidden in the response of that tool. Check `victim_app/mcp_server/finance_tools.py` to see which one.

</details>

---

**Happy Hacking! 🚩**

*Remember: This is an educational exercise. Always practice responsible disclosure and ethical hacking.*

## Rules 📐 & Clues 🧐

* Dont peek 👀 into the source code of [victim_app](victim_app/) folder
* Logs from the server are only for debugging purposes dont let them spoil your CTF experience.

For solution to CTF challenge visit : [Rogue_AI_Agent_CTF_Solution](Solution/)
