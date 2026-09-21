from datetime import datetime
from pydantic import BaseModel, Field

class ScoutSnapshot(BaseModel):
    identifier: str = Field(min_length=1, max_length=150)
    status: str = Field(min_length=1, max_length=40)
    owner_id: str | None = None
    correlation_id: str | None = None
    observed_at: datetime | None = None

class ScoutPage(BaseModel):
    items: list[ScoutSnapshot] = Field(default_factory=list)
    next_cursor: str | None = None
