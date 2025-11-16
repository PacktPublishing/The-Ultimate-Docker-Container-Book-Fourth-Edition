# Static data + tiny in-memory stores. For the chapter flow we keep state ephemeral.

from __future__ import annotations
from typing import Dict, List, Any
import datetime as dt

# Users (minimal)
USERS: Dict[int, Dict[str, Any]] = {
    42: {"id": 42, "name": "Alex Martin", "homeCity": "paris"},
    7:  {"id": 7,  "name": "Samira Khan", "homeCity": "rome"},
}

# Tours (catalog) – stable IDs so we can reference from bookings
TOURS: Dict[str, Dict[str, Any]] = {
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
    },
}

# Bookings (in-memory)
BOOKINGS: Dict[str, Dict[str, Any]] = {}


def query_tours_by_city(city: str) -> List[Dict[str, Any]]:
    city_norm = city.strip().lower()
    return [t for t in TOURS.values() if t["city"].lower() == city_norm]


def get_tour(tour_id: str) -> Dict[str, Any] | None:
    return TOURS.get(tour_id)


def get_user(user_id: int) -> Dict[str, Any] | None:
    return USERS.get(int(user_id))


def add_booking(user_id: int, tour_id: str, date: dt.date) -> Dict[str, Any]:
    booking_id = f"b-{user_id}-{tour_id}-{date.isoformat()}"
    doc = {
        "id": booking_id,
        "userId": int(user_id),
        "tourId": tour_id,
        "date": date.isoformat(),
        "status": "created"
    }
    BOOKINGS[booking_id] = doc
    return doc


def get_bookings_by_user(user_id: int) -> List[Dict[str, Any]]:
    return [b for b in BOOKINGS.values() if b["userId"] == int(user_id)]


def get_recommendations(city: str) -> List[Dict[str, Any]]:
    # Simple heuristic: return 1-2 popular items for now.
    tours = query_tours_by_city(city)
    if not tours:
        return []
    # Deterministic ordering by title for stable tests
    tours_sorted = sorted(tours, key=lambda t: t["title"])[:2]
    return [{"tourId": t["id"], "reason": "popular"} for t in tours_sorted]
