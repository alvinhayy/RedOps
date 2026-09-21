import pytest

from redops_rag.orchestrator import route_task


def test_routes_mobile_task_to_mobile_agent():
    result = route_task("reverse engineer this Android APK with Frida")
    assert result["selected_agents"][0]["agent"] == "mobile_agent"
    assert result["authorization_required"] is True
    assert "redops-rag" in result["selected_agents"][0]["allowed_mcp"]


def test_routes_web3_task_to_web3_agent():
    result = route_task("review a Solidity smart contract on a testnet")
    assert result["selected_agents"][0]["agent"] == "web3_agent"


def test_empty_task_is_rejected():
    with pytest.raises(ValueError):
        route_task("")
