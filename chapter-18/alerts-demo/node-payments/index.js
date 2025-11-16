const express = require("express");

// --- OpenTelemetry imports
const { NodeSDK } =
  require("@opentelemetry/sdk-node");
const { OTLPTraceExporter } =
  require("@opentelemetry/exporter-trace-otlp-http");
const { getNodeAutoInstrumentations } =
  require("@opentelemetry/auto-instrumentations-node");
const { Resource } =
  require("@opentelemetry/resources");
const { SemanticResourceAttributes } =
  require("@opentelemetry/semantic-conventions");

// --- Metrics
const client = require("prom-client");
const REGISTRY = new client.Registry();
client.collectDefaultMetrics({ register: REGISTRY });

const REQS = new client.Counter({
  name: "payments_requests_total",
  help: "Total /pay requests",
  registers: [REGISTRY],
});

const LAT = new client.Histogram({
  name: "payments_request_seconds",
  help: "Latency of /pay",
  buckets: [0.025, 0.05, 0.1, 0.25, 0.5, 1, 2],
  registers: [REGISTRY],
});

const SERVICE_NAME =
  process.env.SERVICE_NAME || "payments-service";
const OTEL_ENDPOINT =
  process.env.OTEL_EXPORTER_OTLP_ENDPOINT ||
  "http://otel-collector:4318";

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: `${OTEL_ENDPOINT}/v1/traces`,
  }),
  resource: new Resource({
    [SemanticResourceAttributes
      .SERVICE_NAME]:
        SERVICE_NAME,
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

Promise.resolve(sdk.start())
  .then(() =>
    console.log("OpenTelemetry SDK started"))
  .catch((err) =>
    console.error("OpenTelemetry SDK error", err));

process.on("SIGTERM", () => {
  Promise.resolve(sdk.shutdown())
    .then(() =>
      console.log("OpenTelemetry SDK shut down"))
    .finally(() => process.exit(0));
});

const app = express();

app.get("/pay", (_req, res) => {
  const end = LAT.startTimer();
  REQS.inc();
  setTimeout(() => {
    end();
    res.send("Payment processed");
  }, 50);
});

// Expose Prometheus metrics
app.get("/metrics", async (_req, res) => {
  try {
    res.set("Content-Type",
      REGISTRY.contentType);
    res.end(await REGISTRY.metrics());
  } catch (e) {
    res.status(500).end(e.toString());
  }
});

app.get("/healthz", (_req, res) => res.send("ok"));

app.listen(8080, () =>
  console.log("payments-service listening on 8080"));
