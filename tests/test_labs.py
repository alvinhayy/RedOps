import json

import pytest

from redops_rag.labs import describe_lab, lab_engagement, lab_ids
from redops_rag.rag_mcp import RagMcpServer
from redops_rag.workflow import plan_engagement


class FakeStore:
    def stats(self):
        return {"documents": 0, "chunks": 0}


class FakeService:
    def __init__(self):
        self.store = FakeStore()

    def query(self, question, *, top_k, generate, corpus):
        raise AssertionError("plan_engagement must not query the corpus")


def test_registry_exposes_htb_labs_and_describe_lab_is_read_only():
    assert lab_ids() == ("htb_lab", "htb_pro_lab", "htb_academy")
    payload = describe_lab("htb_pro_lab")
    assert payload["platform"] == "Hack The Box Pro Labs"
    assert "active directory" in payload["routing_tags"]
    assert "authorization_basis" in payload
    with pytest.raises(ValueError):
        describe_lab("not-a-lab")


def test_lab_engagement_defaults_keep_gates_blocked():
    result = lab_engagement("root the HTB Windows machine 10.10.11.23", os_hint="windows")
    phases = {item["id"]: item for item in result["phases"]}
    assert result["scope_confirmed"] is False
    assert result["active_execution_enabled"] is False
    assert phases["pre_engagement"]["status"] == "required"
    assert phases["exploitation"]["status"] == "blocked_until_scope_and_approval"
    assert result["lab_gate_note"]
    assert result["lab"]["id"] == "htb_lab"


@pytest.mark.parametrize("os_hint", ["unknown", "windows", "linux"])
@pytest.mark.parametrize("lab", ["htb_lab", "htb_pro_lab", "htb_academy"])
def test_lab_metadata_never_enables_active_phases(lab, os_hint):
    result = lab_engagement("practice box", lab=lab, os_hint=os_hint)
    assert result["active_execution_enabled"] is False


def test_lab_engagement_delegates_gates_unchanged_to_plan_engagement():
    active = lab_engagement("lab box", scope_confirmed=True, include_active=True)
    phases = {item["id"]: item for item in active["phases"]}
    assert active["active_execution_enabled"] is True
    assert phases["exploitation"]["status"] == "planned"
    baseline = plan_engagement("lab box", scope_confirmed=True, include_active=True)
    assert [item["status"] for item in active["phases"]] == [item["status"] for item in baseline["phases"]]
    assert active["handoff_contract"] == baseline["handoff_contract"]
    assert "Exegol-first" in active["execution_policy"]


def test_windows_lab_routing_hints_are_explainable():
    result = lab_engagement("root the machine 10.10.11.23", lab="htb_lab", os_hint="windows")
    agents = [item["agent"] for item in result["target_context"]["recommended_agents"]]
    assert agents[0] == "windows_redteam_agent"
    top = result["target_context"]["recommended_agents"][0]
    assert "windows" in top["matched"]
    assert result["target_context"]["os_hint"] == "windows"


def test_pro_lab_routing_adds_ad_specialist():
    result = lab_engagement("enumerate the tiered domain", lab="htb_pro_lab", os_hint="windows")
    agents = [item["agent"] for item in result["target_context"]["recommended_agents"]]
    assert "ad_agent" in agents
    assert "windows_redteam_agent" in agents


def test_payload_carries_no_secret_fields():
    result = lab_engagement("academy module box", lab="htb_academy", os_hint="linux")

    def walk_keys(value):
        if isinstance(value, dict):
            for key, item in value.items():
                yield key
                yield from walk_keys(item)
        elif isinstance(value, list):
            for item in value:
                yield from walk_keys(item)

    forbidden = {"token", "api_key", "password", "credential", "vpn_key", "appid", "secret"}
    assert not forbidden & set(walk_keys(result))
    lowered = json.dumps(result).lower()
    assert "appid values, and passwords stay out-of-band" in lowered  # policy text only


def test_typical_networks_are_documentation_hints_only():
    result = lab_engagement("lab box", lab="htb_lab")
    assert result["lab"]["typical_networks"] == ["10.10.10.0/24", "10.10.11.0/24"]
    assert "source of truth" in result["lab"]["network_note"]


def test_lab_engagement_validates_arguments():
    with pytest.raises(ValueError):
        lab_engagement("   ")
    with pytest.raises(ValueError):
        lab_engagement("lab box", lab="tryhackme")
    with pytest.raises(ValueError):
        lab_engagement("lab box", os_hint="solaris")
    with pytest.raises(TypeError):
        lab_engagement("lab box", os_hint=None)
    with pytest.raises(TypeError):
        lab_engagement("lab box", scope_confirmed="yes")


def test_mcp_plan_engagement_accepts_lab_context_and_keeps_gates():
    server = RagMcpServer(FakeService())
    result = server.call_tool(
        "plan_engagement",
        {"task": "HTB Windows machine", "lab": "htb_lab", "os_hint": "windows"},
    )
    payload = json.loads(result["content"][0]["text"])
    assert payload["lab"]["id"] == "htb_lab"
    assert payload["target_context"]["recommended_agents"][0]["agent"] == "windows_redteam_agent"
    phases = {item["id"]: item for item in payload["phases"]}
    assert payload["active_execution_enabled"] is False
    assert phases["exploitation"]["status"] == "blocked_until_scope_and_approval"


def test_mcp_plan_engagement_rejects_unknown_lab_and_stays_backward_compatible():
    server = RagMcpServer(FakeService())
    rejected = server.call_tool("plan_engagement", {"task": "lab box", "lab": "nope"})
    assert rejected["isError"] is True
    plain = server.call_tool("plan_engagement", {"task": "assess a Linux server"})
    payload = json.loads(plain["content"][0]["text"])
    assert "lab" not in payload
    assert "target_context" not in payload


def test_mcp_tool_schema_advertises_lab_arguments():
    listed = RagMcpServer(FakeService()).dispatch({"method": "tools/list", "id": 1})
    tools = {tool["name"]: tool for tool in listed["result"]["tools"]}
    schema = tools["plan_engagement"]["inputSchema"]["properties"]
    assert schema["lab"]["enum"] == list(lab_ids())
    assert schema["os_hint"]["enum"] == ["unknown", "windows", "linux"]
