# City Tours Catalog Service

A Node.js/Express microservice extracted from the City Tours monolith. This service handles catalog functionality for browsing tours by city.

## 🚀 Features

- **GET /catalog/tours?city={city}** - List tours for a specific city
- **GET /catalog/tours/{tourId}** - Get details for a specific tour
- **GET /health** - Health check endpoint

## 📦 Running Locally

### Prerequisites
- Node.js 16+ 
- npm

### Install & Run
```bash
npm install
npm start
```

The service will start on http://localhost:3000

### Test the Service
```bash
# Health check
curl -s http://localhost:3000/health | jq

# List Paris tours (matches original monolith behavior)
curl -s "http://localhost:3000/catalog/tours?city=paris" | jq

# List Rome tours
curl -s "http://localhost:3000/catalog/tours?city=rome" | jq

# Get specific tour
curl -s http://localhost:3000/catalog/tours/paris-food-101 | jq
```

## 🐳 Running in Docker

### Build
```bash
docker build -t citytours/catalog:1.0 .
```

### Run
```bash
docker run --rm -p 3000:3000 citytours/catalog:1.0
```

## 📊 Data

The service includes the same tour data as the original monolith:
- 2 tours in Paris (street food walk, night cruise)
- 1 tour in Rome (Colosseum & Forum)

## 🔄 Migration from Monolith

This service extracts the `/catalog` functionality from the original Python Flask monolith. It provides the same API contract:

**Original:** `http://localhost:5000/catalog/tours?city=paris`  
**New:** `http://localhost:3000/catalog/tours?city=paris`

Perfect for demonstrating "starving the monolith" pattern with Traefik reverse proxy routing.
