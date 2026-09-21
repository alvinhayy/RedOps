"""Read-only MCP adapter for the RedOps dual-corpus RAG.

The adapter mirrors RedDelta's separate technique/writeup retrieval surfaces while
keeping RedOps provenance and citation metadata intact. It never executes tools or
accepts credentials.
"""
from __future__ import annotations

import json
import sys
from typing import Any

from .orchestrator import route_task
from .service import RagService
from .workflow import plan_engagement

AUTH_WARNING = "Use only with authorized security-testing knowledge and artifacts."
TOOLS = [
    {
        "name": "search_knowledge",
        "description": f"Search technique and methodology knowledge. {AUTH_WARNING}",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "minLength": 1},
                "n_results": {"type": "integer", "minimum": 1, "maximum": 10},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    {
        "name": "search_writeups",
        "description": f"Search solved-engagement/writeup knowledge. {AUTH_WARNING}",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "minLength": 1},
                "n_results": {"type": "integer", "minimum": 1, "maximum": 10},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    {
        "name": "knowledge_stats",
        "description": "Return indexed document/chunk counts by corpus.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "route_task",
        "description": "Select RedOps specialist agents for an authorized task; routing only.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task": {"type": "string", "minLength": 1},
                "limit": {"type": "integer", "minimum": 1, "maximum": 5},
            },
            "required": ["task"],
            "additionalProperties": False,
        },
    },
    {
        "name": "plan_engagement",
        "description": "Build a phase-gated RedOps engagement plan; planning only.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task": {"type": "string", "minLength": 1},
                "scope_confirmed": {"type": "boolean", "default": False},
                "include_active": {"type": "boolean", "default": False},
            },
            "required": ["task"],
            "additionalProperties": False,
        },
    },
]


class RagMcpServer:
    def __init__(self, service: RagService | None = None) -> None:
        self.service = service or RagService()

    @staticmethod
    def _query_args(arguments: dict[str, Any]) -> tuple[str, int]:
        query = arguments.get("query")
        n_results = arguments.get("n_results", 5)
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if isinstance(n_results, bool) or not isinstance(n_results, int) or not 1 <= n_results <= 10:
            raise ValueError("n_results must be an integer between 1 and 10")
        return query.strip(), n_results

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        arguments = arguments or {}
        try:
            if name in {"search_knowledge", "search_writeups"}:
                query, n_results = self._query_args(arguments)
                corpus = "knowledge" if name == "search_knowledge" else "writeups"
                payload = self.service.query(query, top_k=n_results, generate=False, corpus=corpus)
            elif name == "knowledge_stats":
                if arguments:
                    raise ValueError("knowledge_stats accepts no arguments")
                payload = self.service.store.stats()
            elif name == "route_task":
                task = arguments.get("task")
                limit = arguments.get("limit", 3)
                payload = route_task(task, limit)
            elif name == "plan_engagement":
                payload = plan_engagement(
                    arguments.get("task"),
                    scope_confirmed=arguments.get("scope_confirmed", False),
                    include_active=arguments.get("include_active", False),
                )
            else:
                raise ValueError(f"unknown tool: {name}")
            return {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}]}
        except (ValueError, RuntimeError) as exc:
            return {
                "isError": True,
                "content": [{"type": "text", "text": json.dumps({"error": str(exc)})}],
            }

    def dispatch(self, request: dict[str, Any]) -> dict[str, Any] | None:
        method, request_id = request.get("method"), request.get("id")
        if method in {"notifications/initialized", "notifications/cancelled"}:
            return None
        if method == "ping":
            result = {}
        elif method == "initialize":
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "redops-rag", "version": "0.1.0"},
            }
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            params = request.get("params") or {}
            result = self.call_tool(params.get("name", ""), params.get("arguments"))
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": "Method not found"},
            }
        return {"jsonrpc": "2.0", "id": request_id, "result": result}


def serve_stdio(server: RagMcpServer | None = None) -> None:
    server = server or RagMcpServer()
    for line in sys.stdin:
        if not line.strip():
            continue
        response = server.dispatch(json.loads(line))
        if response is not None:
            sys.stdout.write(json.dumps(response, separators=(",", ":"), ensure_ascii=False) + "\n")
            sys.stdout.flush()
