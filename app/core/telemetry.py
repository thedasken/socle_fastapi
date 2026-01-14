from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from prometheus_client import Counter, Histogram, make_asgi_app

from .config import settings

HTTP_REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP Requests", ["method", "endpoint", "http_status"]
)


HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration_seconds", "HTTP Request Duration", ["method", "endpoint"]
)


def setup_telemetry(app):
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    resource = Resource(attributes={SERVICE_NAME: settings.APP_NAME})

    # Exportateur vers la console (pour le test uniquement)
    provider = TracerProvider(resource=resource)

    if settings.ENVIRONMENT.is_deployed:
        processor = BatchSpanProcessor(ConsoleSpanExporter())
        provider.add_span_processor(processor)

    # En PROD, tu ajouteras ici ton OTLPExporter (vers Jaeger/Tempo)
    # elif settings.ENVIRONMENT.is_deployed:
    #     ...

    trace.set_tracer_provider(provider)
