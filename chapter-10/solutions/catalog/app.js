// City Tours Catalog Service
// Node.js/Express microservice extracted from the Python monolith
// Handles /catalog endpoints for tour browsing by city

const express = require('express');
const { queryToursByCity, getTour } = require('./seedData');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Health endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'catalog-service',
    version: '1.0.0',
    time: new Date().toISOString()
  });
});

// Root endpoint with service info
app.get('/', (req, res) => {
  res.json({
    message: 'City Tours Catalog Service',
    endpoints: [
      'GET /health',
      'GET /catalog/tours?city=paris',
      'GET /catalog/tours/{tourId}'
    ]
  });
});

// Main catalog endpoint - list tours by city
app.get('/catalog/tours', (req, res) => {
  const { city } = req.query;
  
  if (!city) {
    return res.status(400).json({
      error: "Missing required query parameter 'city'"
    });
  }
  console.log('Catalog request for city:', city);
  
  const tours = queryToursByCity(city);
  res.json(tours);
});

// Get individual tour (bonus endpoint not in original monolith)
app.get('/catalog/tours/:tourId', (req, res) => {
  const { tourId } = req.params;
  const tour = getTour(tourId);
  
  if (!tour) {
    return res.status(404).json({
      error: `Tour '${tourId}' not found`
    });
  }
  
  res.json(tour);
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Internal server error'
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Endpoint not found'
  });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Catalog service running on http://0.0.0.0:${PORT}`);
  console.log(`📚 Try: curl "http://localhost:${PORT}/catalog/tours?city=paris"`);
});

module.exports = app;
