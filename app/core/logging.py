import json
import logging
from contextvars import ContextVar

from opentelemetry import trace

from .config import settings

# Variable de contexte pour stocker le request_id du cycle de vie de la requête
request_id_context: ContextVar[str] = ContextVar("request_id", default="n/a")


class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_context.get()

        # Récupération du trace_id OTEL actuel
        current_span = trace.get_current_span()
        span_context = current_span.get_span_context()

        if span_context.is_valid:
            # On convertit l'ID hexadécimal en chaîne lisible
            record.trace_id = format(span_context.trace_id, "032x")
        else:
            record.trace_id = "n/a"
        return True


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "rid": getattr(record, "request_id", "n/a"),
            "logger": record.name,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)


def setup_logging():
    handler = logging.StreamHandler()
    handler.addFilter(RequestIDFilter())

    if settings.ENVIRONMENT.is_deployed:
        # Format JSON compact pour la prod
        formatter = JSONFormatter()
    else:
        # Format lisible pour le dev
        log_format = "%(asctime)s | %(levelname)s | [RID: %(request_id)s] [TRACE: %(trace_id)s] | %(name)s:%(lineno)d | %(message)s"
        formatter = logging.Formatter(log_format)

    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

    # Évite les doublons si basicConfig a déjà été appelé
    logging.getLogger("uvicorn.access").disabled = True
