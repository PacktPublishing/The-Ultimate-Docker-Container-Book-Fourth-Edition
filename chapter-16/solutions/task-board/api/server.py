from __future__ import annotations
import os
from dataclasses import dataclass
from typing import List

from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Config via env (works in Docker, docker-compose, Kubernetes)
PORT = int(os.getenv("API_PORT", "8080"))
LOG_LEVEL = os.getenv("API_LOG_LEVEL", "info")
# Prefer DATABASE_URL (e.g., postgres://user:pass@db:5432/taskboard); fall back to SQLite for quick local runs
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME", "taskboard")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    if db_host and db_user and db_pass:
        DATABASE_URL = f"postgresql+psycopg://{db_user}:{db_pass}@{db_host}:5432/{db_name}"
    else:
        DATABASE_URL = f"sqlite+pysqlite:///./{db_name}.db"

app = Flask(__name__)
engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)

INIT_SQL = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'todo'
);
"""

# Initialize database on startup (Flask 3.0+ compatible)
def init_db():
    with engine.begin() as conn:
        conn.execute(text(INIT_SQL))

# Initialize database when the module is loaded
init_db()

@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}, 200
    except OperationalError:
        return {"status": "degraded"}, 503

@app.get("/tasks")
def list_tasks():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, title, status FROM tasks ORDER BY id")).mappings().all()
        return jsonify([dict(r) for r in rows])

@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return {"error": "title is required"}, 400
    status = (data.get("status") or "todo").strip()
    with engine.begin() as conn:
        row = conn.execute(
            text("INSERT INTO tasks (title, status) VALUES (:t, :s) RETURNING id, title, status"),
            {"t": title, "s": status},
        ).mappings().first()
        return dict(row), 201

@app.patch("/tasks/<int:task_id>")
def update_task(task_id: int):
    data = request.get_json(silent=True) or {}
    fields = {}
    if "title" in data:
        fields["title"] = (data["title"] or "").strip()
    if "status" in data:
        fields["status"] = (data["status"] or "").strip()
    if not fields:
        return {"error": "no fields to update"}, 400
    set_clause = ", ".join([f"{k} = :{k}" for k in fields])
    fields["id"] = task_id
    with engine.begin() as conn:
        result = conn.execute(
            text(f"UPDATE tasks SET {set_clause} WHERE id = :id RETURNING id, title, status"),
            fields,
        ).mappings().first()
        if not result:
            return {"error": "not found"}, 404
        return dict(result), 200

@app.delete("/tasks/<int:task_id>")
def delete_task(task_id: int):
    with engine.begin() as conn:
        result = conn.execute(
            text("DELETE FROM tasks WHERE id = :id RETURNING id"),
            {"id": task_id},
        ).first()
        if not result:
            return {"error": "not found"}, 404
        return {"status": "deleted"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)