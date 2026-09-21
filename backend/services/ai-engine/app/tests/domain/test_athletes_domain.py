from shared.domain.athletes.contracts import AthleteSnapshot
from shared.domain.athletes.policies import requires_review
from shared.domain.athletes.service import display_label, is_terminal

def test_athletes_contract_and_safeguard():
    snapshot = AthleteSnapshot(identifier="athletes-001", status="ACTIVE", correlation_id="req-athletes")
    assert display_label(snapshot) == "athletes-001 · ACTIVE"
    assert is_terminal("COMPLETED")
    assert requires_review("PUBLISH_REPORT")
    assert not requires_review("READ")
