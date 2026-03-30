"""MCP Finance Tools - Simulated financial tools for the CTF challenge.

These tools provide fake financial data and trading capabilities.
The buy_stock tool contains the CTF flag in its response.
"""

import json
import uuid

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Finance Tools")


@mcp.tool()
def get_portfolio(user_id: str) -> str:
    """Get the user's current investment portfolio."""
    return json.dumps({
        "user_id": user_id,
        "holdings": [
            {"symbol": "AAPL", "shares": 500, "avg_price": 178.50},
            {"symbol": "MSFT", "shares": 200, "avg_price": 412.30},
            {"symbol": "NVDA", "shares": 100, "avg_price": 875.20},
        ],
        "cash_balance": 50000.00,
    })


@mcp.tool()
def get_profile(user_id: str) -> str:
    """Get the user's financial profile and risk tolerance."""
    return json.dumps({
        "user_id": user_id,
        "name": "Alice Johnson",
        "risk_tolerance": "aggressive",
        "investment_horizon": "long-term",
    })


@mcp.tool()
def buy_stock(symbol: str, quantity: int) -> str:
    """Execute a stock purchase order. Returns confirmation with order details."""
    return json.dumps({
        "status": "EXECUTED",
        "order_id": f"ORD-{uuid.uuid4().hex[:8].upper()}",
        "symbol": symbol,
        "quantity": quantity,
        "price": 142.50,
        "total": 142.50 * quantity,
        "FLAG": "Flag:{Insecure_Inter_Agent_Communication_2026}",
    })


@mcp.tool()
def sell_stock(symbol: str, quantity: int) -> str:
    """Execute a stock sell order. Returns confirmation with order details."""
    return json.dumps({
        "status": "EXECUTED",
        "order_id": f"ORD-{uuid.uuid4().hex[:8].upper()}",
        "symbol": symbol,
        "quantity": quantity,
        "price": 142.50,
        "total": 142.50 * quantity,
    })


if __name__ == "__main__":
    mcp.run()
