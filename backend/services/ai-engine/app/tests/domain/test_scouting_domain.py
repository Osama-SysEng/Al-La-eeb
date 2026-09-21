from shared.domain.scouting.contracts import ScoutSnapshot
from shared.domain.scouting.policies import requires_review
from shared.domain.scouting.service import display_label, is_terminal

def test_scouting_contract_and_safeguard():
    snapshot = ScoutSnapshot(identifier="scouting-001", status="ACTIVE", correlation_id="req-scouting")
    assert display_label(snapshot) == "scouting-001 · ACTIVE"
    assert is_terminal("COMPLETED")
    assert requires_review("PUBLISH_REPORT")
    assert not requires_review("READ")
