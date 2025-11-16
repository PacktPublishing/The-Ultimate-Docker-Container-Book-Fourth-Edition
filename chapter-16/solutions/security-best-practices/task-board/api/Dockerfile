FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

# System deps for psycopg wheels if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py ./

# create an unprivileged user with a fixed UID/GID
RUN useradd -m -u 1000 -s /usr/sbin/nologin appuser \
 && chown -R 1000:1000 /app
USER 1000:1000

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "server:app"]