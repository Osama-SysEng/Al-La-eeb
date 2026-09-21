# Video Governance and Processing Contract

Video analysis is a consent-bound workflow. An upload is not automatically a public highlight, a scouting profile, or a claim of athletic performance. The API requires a verified actor context and active `video_analysis` consent before it accepts a processing request. It stores an idempotency and provenance contract so a client retry does not enqueue duplicate analysis.

| Control | Rule | Production requirement |
|---|---|---|
| Consent | A player must have active, versioned consent for `video_analysis`. | Resolve guardian authority and player relationship in the database; process revocation immediately. |
| Upload | A request must carry an idempotency key and is private by default. | Use pre-signed object-storage upload and malware/media validation before queueing. |
| Provenance | Each job records actor, request key, content fingerprint, and hash. | Persist to `video_analysis_jobs` and include model/version/fingerprint in final reports. |
| Processing | Failures retry only up to the configured limit and must end in reviewable terminal state. | Use a managed queue, GPU scheduling, dead-letter monitoring, and capacity quotas. |
| Retention | Processing carries a retention-days policy. | Run deletion workflows for object storage, derivative clips, vectors, cache, and reports after expiry or revocation. |

> The repository ships no live GPU, biometric, video, object-storage, or notification integration. The current implementation is a contract and development adapter; staging must validate the signed upload path, malware scan, GPU worker isolation, and secure deletion evidence before any real athlete media is processed.
