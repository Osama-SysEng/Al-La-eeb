# Structured Logging — Al-La'eeb

Shared unit: `backend/shared/logging_utils.py` (stdlib only, no new dependencies).
Copied from the canonical template (`C:\pgload\logging_template.py`) with the
default adapted to `SERVICE_NAME=allaeeb-api`.

## Schema (one JSON object per line)

`timestamp` (UTC ISO-8601 ms) + `level` + `service` + `env` + `version`
+ `request_id` + `event` + `message`. Optional merged `fields` are redacted
(password / token / secret / apikey / authorization / cookie / national_id …).

## Configuration (`.env.example`)

| Variable       | Default        | Notes                                            |
|----------------|----------------|--------------------------------------------------|
| `SERVICE_NAME` | `allaeeb-api`  | Override per service (e.g. `allaeeb-gateway`)    |
| `LOG_LEVEL`    | `info`         | `debug` when `ENVIRONMENT` is not `production`   |
| `GIT_SHA`      | `dev`          | Emitted as `version`; set in CI/CD               |
| `ENVIRONMENT`  | `production`   | Emitted as `env`                                 |

## Wired so far (gateway only)

- `backend/api-gateway/app/main.py`: `logging.getLogger("api-gateway")` replaced
  with `get_logger("api-gateway")`. The existing `logging_middleware` now sets
  `request_id_ctx` (propagates `X-Request-ID` or generates one via
  `new_request_id()`), logs one `access: METHOD path -> status in Xs` line per
  request with `http.method/http.path/http.status/duration_ms` fields, and uses
  `logger.exception` on failures. All other gateway behaviour (headers,
  exception handlers, proxy) is unchanged.
- `print` in runtime code replaced with logger calls:
  `services/video-service/app/main.py` (2, existing logger),
  `services/nlp-coach/app/main.py` (2, stdlib `nlp-coach` logger),
  `services/ai-engine/app/pipelines/cv_pipeline.py` (1, stdlib `cv-pipeline` logger).

## Rollout to remaining services

The other services (`auth-service`, `player-service`, `ai-engine`,
`nlp-coach`, `scout-service`, `video-service`) and `api-gateway/app/middleware/rate_limit.py`
still use plain `logging.getLogger(...)` (unstructured, unchanged behaviour —
nothing broken). Rollout plan per service:

1. Set a distinct `SERVICE_NAME` (e.g. `allaeeb-auth`) in its environment.
2. Replace `logging.getLogger("<name>")` with
   `from shared.logging_utils import get_logger; logger = get_logger("<name>")`.
3. In request middleware/lifespan, propagate `X-Request-ID` via `request_id_ctx`
   following the gateway pattern.

## Usage

```python
from shared.logging_utils import get_logger, new_request_id, request_id_ctx

logger = get_logger(__name__)
request_id_ctx.set(new_request_id())
logger.info("startup: service ready", extra={"fields": {"port": 8001}})
```

Never log secrets; the formatter redacts risky keys automatically.
