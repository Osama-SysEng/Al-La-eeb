from dataclasses import dataclass

@dataclass(frozen=True)
class CreateVideo:
    actor_id: str
    correlation_id: str
    reason: str | None = None

@dataclass(frozen=True)
class ReviewVideo:
    identifier: str
    actor_id: str
    decision: str
    reason: str
