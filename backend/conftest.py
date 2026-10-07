"""Backend-root conftest: service-context tests run per-service (see below)."""
import pathlib

_HERE = pathlib.Path(__file__).parent

# These two modules import top-level `app`, which exists once per service
# (services/ai-engine/app, services/auth-service/app). Run them from their
# service directory instead, e.g.:
#   cd services/ai-engine/app && python -m pytest tests/ -q
collect_ignore = [
    str(_HERE / "services" / "ai-engine" / "app" / "tests" / "test_cv.py"),
    str(_HERE / "services" / "auth-service" / "app" / "tests" / "test_auth.py"),
]
