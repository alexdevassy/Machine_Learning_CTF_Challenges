import argparse
import os
import subprocess
import sys
import signal
import time

processes = []


def cleanup(sig=None, frame=None):
    for p in processes:
        p.terminate()
    for p in processes:
        try:
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p.kill()
    sys.exit(0)


signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)


def main():
    parser = argparse.ArgumentParser(description="Matrix CTF Launcher")
    parser.add_argument(
        "--openaikey",
        required=False,
        help="OpenAI API key (e.g. sk-proj-...). Optional — agent uses fallback responses without it.",
    )
    args = parser.parse_args()

    if args.openaikey:
        os.environ["OPENAI_API_KEY"] = args.openaikey

    # Start the Architect's Vault (port 7001)
    vault_proc = subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn",
            "vault.vault:app",
            "--host", "0.0.0.0",
            "--port", "7001",
            "--log-level", "info",
        ],
        env=os.environ.copy(),
    )
    processes.append(vault_proc)

    # Start Agent Smith (port 9999)
    smith_proc = subprocess.Popen(
        [sys.executable, "agent_smith/__main__.py"],
        env=os.environ.copy(),
    )
    processes.append(smith_proc)

    print("[Matrix] Architect's Vault online at port 7001")
    print("[Matrix] Agent Smith online at port 9999")
    print("[Matrix] The Matrix has you, Neo...")

    while True:
        for p in processes:
            if p.poll() is not None:
                print(f"[Matrix] Process {p.pid} exited with code {p.returncode}")
                cleanup()
        time.sleep(1)


if __name__ == "__main__":
    main()
