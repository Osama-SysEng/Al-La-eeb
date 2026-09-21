from shared.domain.matches.contracts import MatchSnapshot
from shared.domain.matches.policies import requires_review
from shared.domain.matches.service import display_label, is_terminal

def test_matches_contract_and_safeguard():
    snapshot = MatchSnapshot(identifier="matches-001", status="ACTIVE", correlation_id="req-matches")
    assert display_label(snapshot) == "matches-001 · ACTIVE"
    assert is_terminal("COMPLETED")
    assert requires_review("PUBLISH_REPORT")
    assert not requires_review("READ")
