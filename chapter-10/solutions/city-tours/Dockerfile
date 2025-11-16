FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
# Install minimal system deps
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py seed_data.py ./
EXPOSE 5000
# Simple healthcheck to verify the app is running
HEALTHCHECK --interval=30s --timeout=3s --start-period=15s \
    CMD curl -fsS http://localhost:5000/health || exit 1
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:create_app()"]