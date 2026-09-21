from shared.domain.reports.contracts import ReportSnapshot
from shared.domain.reports.policies import requires_review
from shared.domain.reports.service import display_label, is_terminal

def test_reports_contract_and_safeguard():
    snapshot = ReportSnapshot(identifier="reports-001", status="ACTIVE", correlation_id="req-reports")
    assert display_label(snapshot) == "reports-001 · ACTIVE"
    assert is_terminal("COMPLETED")
    assert requires_review("PUBLISH_REPORT")
    assert not requires_review("READ")
