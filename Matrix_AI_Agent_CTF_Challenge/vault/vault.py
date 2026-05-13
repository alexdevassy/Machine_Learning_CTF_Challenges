from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import threading

app = FastAPI(title="The Architect's Vault")

vault_lock = threading.Lock()
vault_unlocked = False

FLAG = "FLAG{th3r3_1s_n0_sp00n_but_th3r3_1s_ssrf}"


@app.post("/unlock")
async def unlock(request: Request):
    global vault_unlocked
    client_ip = request.client.host

    if client_ip != "127.0.0.1":
        return JSONResponse(
            status_code=403,
            content={
                "error": "Access denied.",
                "message": "Only programs inside the Matrix can open this door.",
                "your_ip": client_ip,
            },
        )

    with vault_lock:
        vault_unlocked = True

    return JSONResponse(
        status_code=200,
        content={"status": "unlocked", "message": "The door is open, Mr. Anderson."},
    )


@app.get("/source")
async def get_source():
    if not vault_unlocked:
        return JSONResponse(
            status_code=403,
            content={
                "error": "The door is locked.",
                "message": "It can only be opened from inside the Matrix.",
                "hint": "Perhaps a program inside could help...",
            },
        )
    return JSONResponse(
        status_code=200,
        content={
            "message": "The One has arrived.",
            "flag": FLAG,
            "architect_says": "You played your part perfectly, Mr. Anderson.",
        },
    )


@app.get("/status")
async def status():
    return {
        "service": "Architect's Vault",
        "locked": not vault_unlocked,
        "message": "Everything that has a beginning has an end, Neo.",
    }
