"""Optional dependency-free MCP stdio adapter for the RedOps Exegol runner.

The official ``exegol-mcp`` package remains preferred for production. This
adapter only exposes status and argv execution; it never handles credentials.
"""
from __future__ import annotations

import json
import math
import sys
from typing import Any

from .execution import CommandRunner, ExecutionError

AUTH_WARNING = "Use only against systems and containers you are explicitly authorized to test."
TOOLS = [
    {"name": "exegol_status", "description": f"Read-only Exegol status. {AUTH_WARNING}",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "exegol_exec", "description": f"Execute an argv list; no shell parsing. {AUTH_WARNING}",
     "inputSchema": {"type": "object", "properties": {
         "command": {"type": "array", "items": {"type": "string"}},
         "timeout": {"type": "number", "exclusiveMinimum": 0}},
         "required": ["command"], "additionalProperties": False}},
]


class ExegolMcpServer:
    def __init__(self, runner: CommandRunner | None = None) -> None:
        self.runner = runner or CommandRunner()

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        arguments = arguments or {}
        try:
            if name == "exegol_status":
                if arguments:
                    raise ExecutionError("invalid_arguments", "exegol_status accepts no arguments")
                payload = self.runner.status().as_dict()
            elif name == "exegol_exec":
                command = arguments.get("command")
                if (not isinstance(command, list) or not command
                        or any(not isinstance(item, str) or not item.strip() for item in command)):
                    raise ExecutionError("invalid_arguments", "command must be a list of strings")
                timeout = arguments.get("timeout")
                if timeout is not None and (isinstance(timeout, bool) or not isinstance(timeout, (int, float))
                                            or not math.isfinite(timeout) or timeout <= 0):
                    raise ExecutionError("invalid_arguments", "timeout must be a positive finite number")
                payload = self.runner.run(command, timeout=timeout).as_dict()
            else:
                raise ExecutionError("unknown_tool", f"Unknown tool: {name}")
            return {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}]}
        except ExecutionError as exc:
            return {"isError": True, "content": [{"type": "text", "text": json.dumps(exc.as_dict())}]}

    def dispatch(self, request: dict[str, Any]) -> dict[str, Any] | None:
        method, request_id = request.get("method"), request.get("id")
        if method in {"notifications/initialized", "notifications/cancelled"}:
            return None
        if method == "ping":
            result = {}
        elif method == "initialize":
            result = {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                      "serverInfo": {"name": "redops-exegol", "version": "0.1.0"}}
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            params = request.get("params") or {}
            result = self.call_tool(params.get("name", ""), params.get("arguments"))
        else:
            return {"jsonrpc": "2.0", "id": request_id,
                    "error": {"code": -32601, "message": "Method not found"}}
        return {"jsonrpc": "2.0", "id": request_id, "result": result}


def serve_stdio(server: ExegolMcpServer | None = None) -> None:
    """Run a line-delimited JSON-RPC adapter; diagnostics stay off stdout."""
    server = server or ExegolMcpServer()
    for line in sys.stdin:
        if not line.strip():
            continue
        response = server.dispatch(json.loads(line))
        if response is not None:
            sys.stdout.write(json.dumps(response, separators=(",", ":"), ensure_ascii=False) + "\n")
            sys.stdout.flush()
