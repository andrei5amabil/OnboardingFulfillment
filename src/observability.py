# src/observability.py
import os
import logging
from contextlib import nullcontext
from typing import Any

logger = logging.getLogger("uvicorn.error")

ENABLE_OBSERVABILITY = os.getenv("ENABLE_AI_OBSERVABILITY", "true").lower() in ("true", "1", "yes")
CAPTURE_PROMPTS = os.getenv("AI_OBSERVABILITY_CAPTURE_PROMPTS", "false").lower() in ("true", "1", "yes")


def _noop(*args: Any, **kwargs: Any):
    return nullcontext()


workflow = _noop
span = _noop
suppress_tracing = _noop
shutdown_observability = lambda: None

if ENABLE_OBSERVABILITY:
    try:
        import ai_observability
        from ai_observability import workflow as _sdk_workflow
        from ai_observability import span as _sdk_span

        try:
            from opentelemetry.trace import suppress_instrumentation
            suppress_tracing = suppress_instrumentation
        except ImportError:
            suppress_tracing = _noop

        ai_observability.init(
            service_name=os.getenv("OTEL_SERVICE_NAME", "onboarding-agent"),
            service_version=os.getenv("OTEL_SERVICE_VERSION", "1.0.0"),
            deployment_environment=os.getenv("OTEL_DEPLOYMENT_ENVIRONMENT", "development"),
            capture_prompts=CAPTURE_PROMPTS,
        )

        workflow = _sdk_workflow
        span = _sdk_span
        shutdown_observability = ai_observability.shutdown
        logger.info("📡 [Observability] Initialized (capture_prompts: %s)", CAPTURE_PROMPTS)

    except Exception as e:
        logger.warning("⚠️ [Observability] Failed to initialize (%s). Tracing disabled.", e)
        workflow = _noop
        span = _noop
        suppress_tracing = _noop
        shutdown_observability = lambda: None
else:
    logger.info("🔇 [Observability] Tracing disabled via configuration.")