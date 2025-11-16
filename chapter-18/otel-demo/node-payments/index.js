const express = require("express");

// --- OpenTelemetry imports
const { NodeSDK } = require("@opentelemetry/sdk-node");
const { OTLPTraceExporter } =
  require("@opentelemetry/exporter-trace-otlp-http");
const { getNodeAutoInstrumentations } =
  require("@opentelemetry/auto-instrumentations-node");
const { Resource } = require("@opentelemetry/resources");
const { SemanticResourceAttributes } =
  require("@opentelemetry/semantic-conventions");

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
        .SERVICE_NAME]: SERVICE_NAME,
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

// Works whether start() returns void or a Promise
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
  // simulate small processing delay
  setTimeout(() => res.send("Payment processed"), 50);
});

app.get("/healthz", (_req, res) => res.send("ok"));

app.listen(8080, () =>
  console.log("payments-service listening on 8080"));
