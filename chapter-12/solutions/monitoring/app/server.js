const express = require('express');
const client = require('prom-client');
const app = express();
const register = new client.Registry();

const counter = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
});

register.registerMetric(counter);
client.collectDefaultMetrics({ register });

app.get('/', (req, res) => {
  counter.inc();
  res.send('Hello from monitored app!');
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.listen(8080, () => 
  console.log('App running on port 8080'));
