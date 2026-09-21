"""Match bounded context: match context, fixtures, and analytic ownership."""
from .contracts import MatchSnapshot
from .policies import requires_review

__all__ = ["MatchSnapshot", "requires_review"]
