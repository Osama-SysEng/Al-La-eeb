"""Athlete bounded context: player identity, consent, and development baseline."""
from .contracts import AthleteSnapshot
from .policies import requires_review

__all__ = ["AthleteSnapshot", "requires_review"]
