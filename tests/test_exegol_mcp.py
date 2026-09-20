import json

from redops_rag.exegol_mcp import ExegolMcpServer


class FakeResult:
    def __init__(self, payload):
        self.payload = payload

    def as_dict(self):
        return self.payload


class FakeRunner:
    def status(self):
        return FakeResult({"stdout": "ok"})

    def run(self, command, *, timeout=None):
        self.last = (command, timeout)
        return FakeResult({"command": command, "returncode": 0})


def test_tools_status_and_exec():
    runner = FakeRunner()
    server = ExegolMcpServer(runner)
    listed = server.dispatch({"method": "tools/list", "id": 1})
    assert {x["name"] for x in listed["result"]["tools"]} == {"exegol_status", "exegol_exec"}
    assert json.loads(server.call_tool("exegol_status")["content"][0]["text"])["stdout"] == "ok"
    server.call_tool("exegol_exec", {"command": ["nmap", "-sV"], "timeout": 3})
    assert runner.last == (["nmap", "-sV"], 3)


def test_rejects_empty_string_and_injection():
    server = ExegolMcpServer(FakeRunner())
    for command in ([], "id; touch /tmp/pwned"):
        result = server.call_tool("exegol_exec", {"command": command})
        assert result["isError"] is True


def test_unknown_tool_is_error():
    result = ExegolMcpServer(FakeRunner()).call_tool("nope")
    assert result["isError"] is True
