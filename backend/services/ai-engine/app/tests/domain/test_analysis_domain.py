from shared.domain.analysis.contracts import AnalysisSnapshot
from shared.domain.analysis.policies import requires_review
from shared.domain.analysis.service import display_label, is_terminal

def test_analysis_contract_and_safeguard():
    snapshot = AnalysisSnapshot(identifier="analysis-001", status="ACTIVE", correlation_id="req-analysis")
    assert display_label(snapshot) == "analysis-001 · ACTIVE"
    assert is_terminal("COMPLETED")
    assert requires_review("PUBLISH_REPORT")
    assert not requires_review("READ")
