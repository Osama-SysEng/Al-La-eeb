-- Apply from a dedicated migration job after a verified backup; never from API startup.
CREATE TABLE IF NOT EXISTS athlete_video_consents (
  player_id UUID NOT NULL,
  purpose VARCHAR(80) NOT NULL,
  granted_by UUID NOT NULL,
  policy_version VARCHAR(50) NOT NULL,
  granted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at TIMESTAMPTZ,
  revoked_at TIMESTAMPTZ,
  PRIMARY KEY (player_id, purpose)
);

CREATE TABLE IF NOT EXISTS video_analysis_jobs (
  id UUID PRIMARY KEY,
  player_id UUID NOT NULL,
  actor_id UUID NOT NULL,
  idempotency_key VARCHAR(100) NOT NULL,
  filename VARCHAR(255) NOT NULL,
  content_fingerprint CHAR(64) NOT NULL,
  provenance_hash CHAR(64) NOT NULL,
  status VARCHAR(30) NOT NULL,
  retention_days INTEGER NOT NULL,
  attempts INTEGER NOT NULL DEFAULT 0,
  next_retry_at TIMESTAMPTZ,
  terminal_error TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  UNIQUE (player_id, idempotency_key)
);

CREATE TABLE IF NOT EXISTS video_audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  actor_id UUID,
  action VARCHAR(120) NOT NULL,
  entity_id UUID,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS video_delivery_outbox (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  idempotency_key VARCHAR(100) NOT NULL UNIQUE,
  target VARCHAR(80) NOT NULL,
  payload JSONB NOT NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
  attempts INTEGER NOT NULL DEFAULT 0,
  next_retry_at TIMESTAMPTZ,
  last_error TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  processed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_video_jobs_player_created ON video_analysis_jobs(player_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_video_jobs_due ON video_analysis_jobs(status, next_retry_at);
CREATE INDEX IF NOT EXISTS idx_video_audit_actor_created ON video_audit_log(actor_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_video_outbox_due ON video_delivery_outbox(status, next_retry_at);
