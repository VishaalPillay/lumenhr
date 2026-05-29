"""
LumenHR MCP Server — FastAPI Application Entry Point.

Start with:
    uvicorn mcp_server.main:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI

from mcp_server.tools.hr_read import router as hr_read_router

app = FastAPI(
    title="LumenHR MCP Server",
    version="0.1.0",
    description=(
        "Privacy-first workforce intelligence agent. Exposes Model Context "
        "Protocol (MCP) endpoints for M365 Copilot Chat integration."
    ),
)

# ── Route registration ────────────────────────────────────────────────────────

app.include_router(hr_read_router)
