const express = require('express');
const app = express();

app.get('/', (req, res) => {
  console.log(`[INFO] Request received at /`);
  res.send('Hello from Node.js API');
});

app.get('/error', (req, res) => {
  console.error('[ERROR] Simulated error occurred!');
  res.status(500).send('Something went wrong');
});

app.listen(8080, '0.0.0.0', () => {
  console.log('Node API running on port 8080');
});
