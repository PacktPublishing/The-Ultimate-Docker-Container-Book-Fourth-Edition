// Static tour data - mirroring the Python seed_data.py for catalog functionality

const TOURS = {
  "paris-food-101": {
    "id": "paris-food-101",
    "city": "paris",
    "title": "Paris Street Food Walk",
    "durationHours": 3,
    "price": 49.0,
    "tags": ["food", "walking", "local"]
  },
  "paris-night-views": {
    "id": "paris-night-views",
    "city": "paris",
    "title": "Seine Night Cruise & Skyline",
    "durationHours": 2,
    "price": 59.0,
    "tags": ["boat", "night", "photography"]
  },
  "rome-history-core": {
    "id": "rome-history-core",
    "city": "rome",
    "title": "Colosseum & Forum Essentials",
    "durationHours": 4,
    "price": 69.0,
    "tags": ["history", "walking"]
  }
};

function queryToursByCity(city) {
  const cityNorm = city.trim().toLowerCase();
  return Object.values(TOURS).filter(tour => tour.city.toLowerCase() === cityNorm);
}

function getTour(tourId) {
  return TOURS[tourId] || null;
}

module.exports = {
  queryToursByCity,
  getTour,
  TOURS
};
