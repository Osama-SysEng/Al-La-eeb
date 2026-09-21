# Al-La'eeb Operational Hardening

The video pipeline now has a development governance adapter that requires a verified actor context, active video-analysis consent, a private-default upload, and an idempotency key. It records request provenance and retention policy before asynchronous analysis. It does not upload media or start a GPU model without a separate approved storage and worker deployment.

| Gate | Required staging evidence |
|---|---|
| Consent | Guardian/player relation, policy version, grant/revocation audit, and secure deletion verification. |
| Storage | Signed upload URL, malware/media validation, encryption, private retrieval, and expiry. |
| GPU | Isolated worker, queue quota, model version capture, retry/dead-letter monitor, and capacity tests. |
| Reports | Actor entitlement, provenance/model version disclosure, and no public publication by ingest API. |
| Load | Run `tools/load_probe.py` only against approved staging; it blocks remote targets by default. |

> Tests cover governance contracts only. OpenCV, MediaPipe, GPU inference, object storage, biometric verification, and real streaming require a separate staging environment and must not be inferred from this source package.
