# City Tours – Monolith Demo

A small, self-contained **City Tours** web application built with Flask, designed as a practical example for  
Chapter 10: *Using Single Host Networking* of **The Ultimate Docker Container Book**.

This monolith will serve as the starting point for demonstrating **HTTP-level routing using a reverse proxy** (Traefik) and the process of “starving the monolith” by extracting services into independent containers.

---

## ✨ Features

- **Catalog** – Browse tours by city  
- **Bookings** – Create and view tour bookings  
- **Users** – Simple user profile lookups  
- **Recommendations** – Suggested tours per city  
- **Payments** – Stub checkout endpoint for future extraction  

All endpoints live under clear, service-like URL prefixes to make later path-based routing trivial.

---

## 📂 Project Structure

```
.
├── app.py               # Flask application
├── seed_data.py         # Static data and in-memory stores
├── requirements.txt     # Python dependencies
├── Dockerfile           # Production container build
└── README.md
```

---

## 🚀 Running Locally (Bare Metal)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=app.py
export FLASK_ENV=development
flask run -h 0.0.0.0 -p 5000
```

Access the app at: [http://localhost:5000](http://localhost:5000)

---

## 📦 Running in Docker

### Build
```bash
docker build -t citytours/monolith:1.0 .
```

### Run
```bash
docker run --rm -p 5000:5000 citytours/monolith:1.0
```

---

## 🔍 Example Requests

- **Health check**
  ```bash
  curl -s http://localhost:5000/health | jq
  ```

- **List Paris tours**
  ```bash
  curl -s "http://localhost:5000/catalog/tours?city=paris" | jq
  ```

- **Create booking**
  ```bash
  curl -s -X POST http://localhost:5000/bookings \
    -H "Content-Type: application/json" \
    -d '{
      "tourId": "paris-food-101",
      "userId": 42,
      "date": "2025-08-15"
    }' | jq
  ```

- **Get bookings for user 42**
  ```bash
  curl -s "http://localhost:5000/bookings?userId=42" | jq
  ```

- **Get recommendations for Paris**
  ```bash
  curl -s "http://localhost:5000/recommendations?city=paris" | jq
  ```

---

## 🛠 Educational Flow

This monolith is **Step 1** in the Chapter 10 demo journey:

1. **Run the monolith** in Docker on a custom bridge network.  
2. **Publish ports** and verify access from the host.  
3. **Introduce Traefik** as a reverse proxy with HTTP-level routing to `/catalog`, `/bookings`, etc.  
4. **Extract services**:
   - Move `/catalog` into its own container.
   - Route `/catalog/*` through Traefik while other routes still hit the monolith.
5. Repeat until the monolith is fully decomposed into independent services.

This approach demonstrates the “starve the monolith” pattern while maintaining a seamless client experience.

---

## 📚 Related Book Sections

- **Container Network Model** – Isolation, connectivity, and network types  
- **Port Management** – Publishing and binding  
- **HTTP-level Routing using a Reverse Proxy** – Traefik path-based routing  
- **Starving the Monolith** – Gradual service extraction

---

## 📝 License

For educational use with *The Ultimate Docker Container Book*.  
Not intended for production deployments.
