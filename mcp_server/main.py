"""
LumenHR MCP Server — FastAPI Application Entry Point.

Start with:
    uvicorn mcp_server.main:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI

from mcp_server.tools.hr_read import router as hr_read_router
from mcp_server.tools.hr_write import router as hr_write_router
from mcp_server.tools.employee_tools import router as employee_tools_router
from mcp_server.tools.org_tools import router as org_tools_router

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
app.include_router(hr_write_router)
app.include_router(employee_tools_router)
app.include_router(org_tools_router)


# ── Health check ──────────────────────────────────────────────────────────────


@app.get("/health")
def health():
    return {"status": "healthy", "version": "0.1.0"}