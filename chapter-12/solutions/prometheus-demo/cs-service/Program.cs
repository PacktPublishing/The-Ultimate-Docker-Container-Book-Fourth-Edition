using Prometheus;

var counter = Metrics.CreateCounter(
  "cs_requests_total",
  "Total number of requests");

var app = WebApplication.Create();
app.MapGet("/", () =>
{
  counter.Inc();
  return "Hello from C# service!";
});
app.MapMetrics();
app.Run("http://0.0.0.0:8083");
