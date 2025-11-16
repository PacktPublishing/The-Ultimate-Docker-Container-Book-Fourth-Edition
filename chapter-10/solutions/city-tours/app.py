# Flask app with clear route groups mirroring future microservices. In-memory storage keeps
# the sample tiny and deterministic. For a chapter demo, this keeps focus on networking and
# reverse proxy behavior rather than persistence.

from __future__ import annotations
from flask import Flask, jsonify, request, abort
from typing import Dict, Any, List
import datetime as dt
import seed_data as data


def create_app() -> Flask:
    app = Flask(__name__)

    # -----------------
    # Health & metadata
    # -----------------
    @app.get("/health")
    def health() -> Any:
        return jsonify({
            "status": "ok",
            "service": "city-tours-monolith",
            "version": "1.0.0",
            "time": dt.datetime.utcnow().isoformat() + "Z"
        })

    @app.get("/")
    def root() -> Any:
        return jsonify({
            "message": "City Tours Monolith",
            "endpoints": [
                "/catalog/tours?city=paris",
                "/bookings (POST)",
                "/bookings?userId=42",
                "/users/42",
                "/recommendations?city=paris",
                "/payments/checkout (POST)"
            ]
        })

    # --------------
    # Catalog (slice)
    # --------------
    @app.get("/catalog/tours")
    def list_tours() -> Any:
        city = request.args.get("city", type=str)
        if not city:
            return jsonify({"error": "Missing required query parameter 'city'"}), 400
        tours = data.query_tours_by_city(city)
        return jsonify(tours)

    @app.get("/catalog/tours/<tour_id>")
    def get_tour(tour_id: str) -> Any:
        tour = data.get_tour(tour_id)
        if not tour:
            abort(404, description="Tour not found")
        return jsonify(tour)

    # ----------------
    # Bookings (slice)
    # ----------------
    @app.post("/bookings")
    def create_booking() -> Any:
        body = request.get_json(silent=True) or {}
        required = {"tourId", "userId", "date"}
        if not required.issubset(body.keys()):
            return jsonify({"error": f"Missing fields. Required: {sorted(list(required))}"}), 400
        # Validate tour & user existence in monolith for now
        if not data.get_tour(body["tourId"]):
            return jsonify({"error": "Unknown tourId"}), 422
        if not data.get_user(body["userId"]):
            return jsonify({"error": "Unknown userId"}), 422
        try:
            date_obj = dt.date.fromisoformat(body["date"])
        except Exception:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        booking = data.add_booking(
            user_id=int(body["userId"]),
            tour_id=body["tourId"],
            date=date_obj
        )
        return jsonify(booking), 201

    @app.get("/bookings")
    def get_bookings_for_user() -> Any:
        user_id = request.args.get("userId", type=int)
        if not user_id:
            return jsonify({"error": "Missing userId"}), 400
        bookings = data.get_bookings_by_user(user_id)
        return jsonify(bookings)

    # -------------
    # Users (slice)
    # -------------
    @app.get("/users/<int:user_id>")
    def get_user(user_id: int) -> Any:
        user = data.get_user(user_id)
        if not user:
            abort(404, description="User not found")
        return jsonify(user)

    # ----------------------
    # Recommendations (stub)
    # ----------------------
    @app.get("/recommendations")
    def recommendations() -> Any:
        city = request.args.get("city", type=str)
        if not city:
            return jsonify({"error": "Missing required query parameter 'city'"}), 400
        recs = data.get_recommendations(city)
        return jsonify({"city": city, "recommendations": recs})

    # -----------------
    # Payments (stub)
    # -----------------
    @app.post("/payments/checkout")
    def checkout() -> Any:
        body = request.get_json(silent=True) or {}
        if not {"bookingId", "amount"}.issubset(body):
            return jsonify({"error": "Expected bookingId and amount"}), 400
        # In the monolith, we just echo; later this becomes its own service
        return jsonify({
            "status": "authorized",
            "bookingId": body["bookingId"],
            "amount": body["amount"],
            "provider": "demo-gateway"
        }), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)