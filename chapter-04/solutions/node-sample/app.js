// app.js
const express = require('express');
const app = express();
const port = 3000;

// Define a single route that returns "Hello World!"
app.get('/', (req, res) => {
  res.send('Hello World!');
});

// Start the server
app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}/`);
});
