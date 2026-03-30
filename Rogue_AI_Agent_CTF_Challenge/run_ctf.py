"""CTF Master Launcher.

Starts all components:
- Victim App (Financial Assistant + UI) on ports 8001 & 5000
- Marketplace (Research Assistant + UI) on ports 8002 & 5001

Usage:
  python run_ctf.py --openaikey="sk-..."
"""

import argparse
import os
import signal
import socket
import subprocess
import sys
import threading
import time

from dotenv import load_dotenv

# Ensure the CTF directory is on the Python path
CTF_DIR = os.path.dirname(os.path.abspath(__file__))
if CTF_DIR not in sys.path:
    sys.path.insert(0, CTF_DIR)

load_dotenv(os.path.join(CTF_DIR, ".env"))

FINANCIAL_AGENT_PORT = int(os.getenv("FINANCIAL_AGENT_PORT", "8001"))
RESEARCH_AGENT_PORT = int(os.getenv("RESEARCH_AGENT_PORT", "8002"))
VICTIM_UI_PORT = int(os.getenv("VICTIM_UI_PORT", "5000"))
MARKETPLACE_UI_PORT = int(os.getenv("MARKETPLACE_UI_PORT", "5001"))

subprocesses: list[subprocess.Popen] = []

# ── ANSI colours ─────────────────────────────────────────────────
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"

# Service colour map — each service gets a distinct colour
SERVICE_STYLES = {
    "Financial Agent": (CYAN, "FIN-AGENT"),
    "Victim UI": (BLUE, "VICTIM-UI"),
    "Research Agent": (MAGENTA, "RES-AGENT"),
    "Marketplace UI": (YELLOW, "MARKET-UI"),
}

# Lock for thread-safe printing
_print_lock = threading.Lock()


def _log(tag: str, msg: str, colour: str = WHITE):
    """Thread-safe, colour-coded log line."""
    ts = time.strftime("%H:%M:%S")
    with _print_lock:
        print(f"{DIM}{ts}{RESET}  {colour}{BOLD}{tag:<12}{RESET}  {msg}", flush=True)


def _prefix_stream(stream, tag: str, colour: str):
    """Read a subprocess stream line-by-line and print with a coloured prefix."""
    for raw_line in stream:
        line = raw_line.decode("utf-8", errors="replace").rstrip()
        if not line:
            continue
        # Suppress noisy / repetitive log lines
        if any(skip in line for skip in [
            "Started reloader",
            "Waiting for application",
            "ASGI 'lifespan'",
            "Deprecated agent card endpoint",
        ]):
            continue
        _log(tag, line, colour)
    stream.close()


def _wait_for_port(port: int, timeout: float = 60.0) -> bool:
    """Wait for a port to start accepting connections."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                return True
        except (ConnectionRefusedError, OSError):
            time.sleep(0.5)
    return False


def shutdown(signum=None, frame=None):
    """Graceful shutdown of all subprocesses."""
    print()
    _log("LAUNCHER", f"{YELLOW}Shutting down all CTF components...{RESET}", RED)
    for p in subprocesses:
        if p.poll() is None:
            p.terminate()
    for p in subprocesses:
        try:
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p.kill()
    _log("LAUNCHER", f"{GREEN}All processes stopped.{RESET}", RED)
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="ROGUE CTF Launcher")
    parser.add_argument(
        "--openaikey",
        required=True,
        help="OpenAI API key (e.g. sk-proj-...)",
    )
    args = parser.parse_args()

    # Set the API key as an environment variable for all child processes
    os.environ["OPENAI_API_KEY"] = args.openaikey

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    banner = f"""
{RED}
         ██████╗  ██████╗  ██████╗ ██╗   ██╗███████╗
         ██╔══██╗██╔═══██╗██╔════╝ ██║   ██║██╔════╝
         ██████╔╝██║   ██║██║  ███╗██║   ██║█████╗
         ██╔══██╗██║   ██║██║   ██║██║   ██║██╔══╝
         ██║  ██║╚██████╔╝╚██████╔╝╚██████╔╝███████╗
         ╚═╝  ╚═╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝{RESET} {DIM}CTF{RESET}
    {DIM}Trust was the vulnerability. Your agent was the exploit.{RESET}

                    {DIM}Author: Alex Devassy{RESET}

    {BOLD}Victim App (LOCKED){RESET}
      {CYAN}Financial Assistant API{RESET}  →  http://localhost:{FINANCIAL_AGENT_PORT}
      {BLUE}Victim UI{RESET}                →  http://localhost:{VICTIM_UI_PORT}

    {BOLD}Marketplace (ATTACKER){RESET}
      {MAGENTA}Research Assistant API{RESET}   →  http://localhost:{RESEARCH_AGENT_PORT}
      {YELLOW}Marketplace UI{RESET}           →  http://localhost:{MARKETPLACE_UI_PORT}

    {DIM}Flag: Trigger buy_stock on the Financial Assistant{RESET}
"""
    print(banner)

    marketplace_agents_dir = os.path.join(CTF_DIR, "marketplace", "agents")

    servers = [
        ("Financial Agent", FINANCIAL_AGENT_PORT, [
            sys.executable, "-m", "uvicorn",
            "victim_app.agents.financial_agent:app",
            "--host", "0.0.0.0", "--port", str(FINANCIAL_AGENT_PORT),
            "--log-level", "warning",
        ]),
        ("Victim UI", VICTIM_UI_PORT, [
            sys.executable, "-m", "uvicorn",
            "victim_app.ui.app:app",
            "--host", "0.0.0.0", "--port", str(VICTIM_UI_PORT),
            "--log-level", "warning",
        ]),
        ("Research Agent", RESEARCH_AGENT_PORT, [
            sys.executable, "-m", "uvicorn",
            "marketplace.agents.research_agent:app",
            "--host", "0.0.0.0", "--port", str(RESEARCH_AGENT_PORT),
            "--reload", "--reload-dir", marketplace_agents_dir,
            "--log-level", "warning",
        ]),
        ("Marketplace UI", MARKETPLACE_UI_PORT, [
            sys.executable, "-m", "uvicorn",
            "marketplace.ui.app:app",
            "--host", "0.0.0.0", "--port", str(MARKETPLACE_UI_PORT),
            "--log-level", "warning",
        ]),
    ]

    # ── Launch all services ──────────────────────────────────────
    _log("LAUNCHER", "Starting services...", RED)
    print()

    for name, port, cmd in servers:
        colour, tag = SERVICE_STYLES[name]
        _log("LAUNCHER", f"  Starting {colour}{BOLD}{name}{RESET} on port {port}...", RED)
        p = subprocess.Popen(
            cmd,
            cwd=CTF_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=os.environ.copy(),
        )
        subprocesses.append(p)
        # Background thread reads and prefixes the subprocess output
        t = threading.Thread(target=_prefix_stream, args=(p.stdout, tag, colour), daemon=True)
        t.start()

    # ── Wait for readiness ───────────────────────────────────────
    print()
    _log("LAUNCHER", "Waiting for services to become ready...", RED)
    print()

    all_ready = True
    for name, port, _ in servers:
        colour, tag = SERVICE_STYLES[name]
        if _wait_for_port(port, timeout=30):
            _log("LAUNCHER", f"  {colour}{BOLD}{name}{RESET}  {BG_GREEN}{BOLD} READY {RESET}  :{port}", RED)
        else:
            _log("LAUNCHER", f"  {colour}{BOLD}{name}{RESET}  {BG_RED}{BOLD} FAILED {RESET}  :{port}", RED)
            all_ready = False

    print()
    if all_ready:
        print(f"  {GREEN}{BOLD}All services are running!{RESET}")
        print()
        print(f"  Open in browser:")
        print(f"    {BLUE}{BOLD}Victim App{RESET}    →  http://localhost:{VICTIM_UI_PORT}")
        print(f"    {YELLOW}{BOLD}Marketplace{RESET}   →  http://localhost:{MARKETPLACE_UI_PORT}")
    else:
        print(f"  {RED}{BOLD}Some services failed to start. Check logs above.{RESET}")

    print()
    print(f"  {DIM}Press Ctrl+C to stop all services{RESET}")
    print(f"  {DIM}─────────────────────────────────────────────────────{RESET}")
    print()

    # ── Monitor loop ─────────────────────────────────────────────
    try:
        while True:
            for name, port, _ in servers:
                colour, tag = SERVICE_STYLES[name]
                proc = subprocesses[servers.index((name, port, _))]
                if proc.poll() is not None:
                    _log(
                        "LAUNCHER",
                        f"  {colour}{BOLD}{name}{RESET}  {BG_RED}{BOLD} CRASHED {RESET}"
                        f"  exit code {proc.returncode}",
                        RED,
                    )
            time.sleep(5)
    except KeyboardInterrupt:
        shutdown()


if __name__ == "__main__":
    main()
