from shared.domain.video.contracts import VideoSnapshot
from shared.domain.video.policies import requires_review
from shared.domain.video.service import display_label, is_terminal

def test_video_contract_and_safeguard():
    snapshot = VideoSnapshot(identifier="video-001", status="ACTIVE", correlation_id="req-video")
    assert display_label(snapshot) == "video-001 · ACTIVE"
    assert is_terminal("COMPLETED")
    assert requires_review("PUBLISH_REPORT")
    assert not requires_review("READ")
