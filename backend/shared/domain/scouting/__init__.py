"""Scout bounded context: discovery, shortlists, and responsible comparison."""
from .contracts import ScoutSnapshot
from .policies import requires_review

__all__ = ["ScoutSnapshot", "requires_review"]
