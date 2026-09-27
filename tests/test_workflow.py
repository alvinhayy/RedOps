import pytest

from redops_rag.workflow import phase, plan_engagement


def test_workflow_requires_scope_before_active_phases():
    result = plan_engagement("assess a Linux server")
    phases = {item["id"]: item for item in result["phases"]}
    assert result["active_execution_enabled"] is False
    assert phases["pre_engagement"]["status"] == "required"
    assert phases["exploitation"]["status"] == "blocked_until_scope_and_approval"


def test_workflow_enables_active_plan_only_with_both_flags():
    result = plan_engagement("assess a Windows Server", scope_confirmed=True, include_active=True)
    phases = {item["id"]: item for item in result["phases"]}
    assert result["active_execution_enabled"] is True
    assert phases["exploitation"]["status"] == "planned"
    assert phases["lateral_movement"]["status"] == "planned"


def test_workflow_has_report_terminal_and_known_phase_lookup():
    assert phase("post_engagement").next_phases == ()
    with pytest.raises(ValueError):
        phase("not-a-phase")


def test_workflow_reports_scope_record_without_unlocking_gates(tmp_path):
    record = tmp_path / "scope.md"
    record.write_text(
        """# Scope record\n\n## Authorization\nCoordinator approval.\n\n"
        "## Target inventory\n10.129.43.144 — In scope: YES\n\n"
        "## Phase approvals\n- information_gathering\n""",
        encoding="utf-8",
    )
    result = plan_engagement("audit a Windows AD host", scope_record=record)
    assert result["scope_record"]["valid_structure"] is True
    assert result["scope_record"]["targets"] == ["10.129.43.144"]
    assert result["scope_confirmed"] is False
    assert result["active_execution_enabled"] is False


def test_workflow_adds_ad_and_supply_chain_niches():
    result = plan_engagement("review VSIX supply chain ACL over signed LDAP")
    assert "ad" in result["niche_hints"]
    assert "supply_chain" in result["niche_hints"]
