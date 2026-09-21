from shared.domain.safety.contracts import SafetySnapshot
from shared.domain.safety.policies import requires_review
from shared.domain.safety.service import display_label, is_terminal

def test_safety_contract_and_safeguard():
    snapshot = SafetySnapshot(identifier="safety-001", status="ACTIVE", correlation_id="req-safety")
    assert display_label(snapshot) == "safety-001 · ACTIVE"
    assert is_terminal("COMPLETED")
    assert requires_review("PUBLISH_REPORT")
    assert not requires_review("READ")
