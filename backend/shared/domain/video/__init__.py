"""Video bounded context: ingestion, clips, retention, and access boundaries."""
from .contracts import VideoSnapshot
from .policies import requires_review

__all__ = ["VideoSnapshot", "requires_review"]
