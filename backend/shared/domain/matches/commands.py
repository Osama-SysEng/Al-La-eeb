from dataclasses import dataclass

@dataclass(frozen=True)
class CreateMatch:
    actor_id: str
    correlation_id: str
    reason: str | None = None

@dataclass(frozen=True)
class ReviewMatch:
    identifier: str
    actor_id: str
    decision: str
    reason: str
