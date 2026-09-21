"""Development adapter for consent, provenance, and video job lifecycle.

Production repositories must persist this contract in PostgreSQL and object storage.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from uuid import uuid4


@dataclass
class ConsentRecord:
    player_id: str
    purpose: str
    granted_by: str
    policy_version: str
    expires_at: datetime | None = None
    revoked_at: datetime | None = None

    def active(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return self.revoked_at is None and (self.expires_at is None or self.expires_at > now)


@dataclass
class VideoLedger:
    consents: dict[tuple[str, str], ConsentRecord] = field(default_factory=dict)
    jobs_by_key: dict[tuple[str, str], dict] = field(default_factory=dict)
    jobs_by_id: dict[str, dict] = field(default_factory=dict)

    def grant_consent(self, record: ConsentRecord) -> None:
        self.consents[(record.player_id, record.purpose)] = record

    def revoke_consent(self, player_id: str, purpose: str) -> None:
        record = self.consents.get((player_id, purpose))
        if record: record.revoked_at = datetime.now(timezone.utc)

    def has_consent(self, player_id: str, purpose: str) -> bool:
        return bool(self.consents.get((player_id, purpose)) and self.consents[(player_id, purpose)].active())

    def register_job(self, player_id: str, idempotency_key: str, actor_id: str, filename: str, content_fingerprint: str, retention_days: int) -> tuple[dict, bool]:
        key = (player_id, idempotency_key)
        if key in self.jobs_by_key: return self.jobs_by_key[key], True
        job = {'video_id': str(uuid4()), 'player_id': player_id, 'actor_id': actor_id, 'idempotency_key': idempotency_key, 'filename': filename, 'content_fingerprint': content_fingerprint, 'status': 'QUEUED', 'retention_days': retention_days, 'created_at': datetime.now(timezone.utc).isoformat(), 'provenance_hash': sha256(f'{player_id}:{actor_id}:{idempotency_key}:{content_fingerprint}'.encode()).hexdigest()}
        self.jobs_by_key[key] = job; self.jobs_by_id[job['video_id']] = job
        return job, False


ledger = VideoLedger()
