from flask import Flask, request, jsonify
import requests
import os

# --- OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.instrumentation.flask import (
    FlaskInstrumentor,
)
from opentelemetry.instrumentation.requests import (
    RequestsInstrumentor,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)

SERVICE = os.getenv("SERVICE_NAME", "orders-service")
OTEL_ENDPOINT = os.getenv(
    "OTEL_EXPORTER_OTLP_ENDPOINT",
    "http://otel-collector:4318",
)

# --- Configure tracer provider
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: SERVICE})
    )
)
tracer_provider = trace.get_tracer_provider()
tracer_provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint=f"{OTEL_ENDPOINT}/v1/traces"
        )
    )
)

app = Flask(__name__)

# Auto-instrument Flask + outgoing requests
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


@app.route("/order", methods=["POST"])
def order():
    payload = request.get_json(force=True, silent=True) or {}

    # Simulate a downstream call to payments-service
    try:
        resp = requests.get(
            "http://payments-service:8080/pay",
            timeout=2,
        )
        pay_status = {
            "payments_status": resp.text,
            "payments_code": resp.status_code,
        }
    except Exception as ex:
        pay_status = {
            "payments_status": f"error: {ex}",
            "payments_code": 500,
        }

    return jsonify(
        {
            "service": SERVICE,
            "message": "Order received",
            "payload": payload,
            "downstream": pay_status,
        }
    )


@app.route("/healthz")
def health():
    return "ok"


if __name__ == "__main__":
    # Flask dev server; in container we use it directly
    app.run(host="0.0.0.0", port=8080)