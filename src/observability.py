import os
import logging
from contextlib import nullcontext
from typing import Any

logger = logging.getLogger("uvicorn.error")

ENABLE_OBSERVABILITY = os.getenv("ENABLE_AI_OBSERVABILITY", "true").lower() in ("true", "1", "yes")

if ENABLE_OBSERVABILITY:
    try:
        import ai_observability
        from ai_observability import workflow as _sdk_workflow
        from ai_observability import span as _sdk_span

        ai_observability.init(
            service_name=os.getenv("OTEL_SERVICE_NAME", "onboarding-agent"),
            service_version=os.getenv("OTEL_SERVICE_VERSION", "1.0.0"),
            deployment_environment=os.getenv("OTEL_DEPLOYMENT_ENVIRONMENT", "development"),
        )
        logger.info("📡 [Observability] SDK initialized and tracing enabled.")

        workflow = _sdk_workflow
        span = _sdk_span

        def shutdown_observability():
            ai_observability.shutdown()

    except ImportError:
        logger.warning("⚠️ [Observability] ai-observability-sdk not installed. Falling back to no-op.")
        ENABLE_OBSERVABILITY = False

if not ENABLE_OBSERVABILITY:
    logger.info("🔇 [Observability] Tracing is disabled via configuration.")

    def workflow(*args: Any, **kwargs: Any):
        """No-op context manager when observability is turned off."""
        return nullcontext()

    def span(*args: Any, **kwargs: Any):
        """No-op context manager/decorator for spans."""
        return nullcontext()

    def shutdown_observability():
        pass