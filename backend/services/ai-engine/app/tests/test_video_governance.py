from datetime import datetime, timedelta, timezone
from shared.video_governance import ConsentRecord, VideoLedger

def test_video_job_requires_active_consent_and_replays_by_key():
    ledger = VideoLedger()
    assert not ledger.has_consent('player-1', 'video_analysis')
    ledger.grant_consent(ConsentRecord('player-1', 'video_analysis', 'guardian-1', '2026-08'))
    assert ledger.has_consent('player-1', 'video_analysis')
    first, replay = ledger.register_job('player-1', 'upload-key-001', 'guardian-1', 'clip.mp4', 'fingerprint', 90)
    second, replay2 = ledger.register_job('player-1', 'upload-key-001', 'guardian-1', 'clip.mp4', 'fingerprint', 90)
    assert not replay and replay2 and first['video_id'] == second['video_id']

def test_expired_consent_blocks_analysis():
    ledger = VideoLedger()
    ledger.grant_consent(ConsentRecord('player-1', 'video_analysis', 'guardian-1', '2026-08', expires_at=datetime.now(timezone.utc) - timedelta(seconds=1)))
    assert not ledger.has_consent('player-1', 'video_analysis')
