import pytest

from redops_rag.orchestrator import route_task


def test_routes_mobile_task_to_mobile_agent():
    result = route_task("reverse engineer this Android APK with Frida")
    assert result["selected_agents"][0]["agent"] == "mobile_agent"
    assert result["authorization_required"] is True
    assert "redops-rag" in result["selected_agents"][0]["allowed_mcp"]
    assert "mobile_agent" in result["selected_agents"][0]["workspace_agents"]


def test_routes_web3_task_to_web3_agent():
    result = route_task("review a Solidity smart contract on a testnet")
    assert result["selected_agents"][0]["agent"] == "web3_agent"


def test_empty_task_is_rejected():
    with pytest.raises(ValueError):
        route_task("")


def test_routes_checkpoint_artifacts_to_ad_and_windows_specialists():
    result = route_task("enumerate signed LDAP ACLs for GenericWrite and VSIX supply chain")
    agents = [item["agent"] for item in result["selected_agents"]]
    assert "ad_agent" in agents
    assert "windows_redteam_agent" in agents
    assert result["workspace_agent_graph"][:3] == ["recon", "web-recon", "web-exploit"]
    selected = {item["agent"]: item for item in result["selected_agents"]}
    assert "ad-enum" in selected["ad_agent"]["workspace_agents"]
