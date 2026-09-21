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
