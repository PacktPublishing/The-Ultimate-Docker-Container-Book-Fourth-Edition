FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# opentelemetry config via env; can be overridden in Kubernetes
ENV SERVICE_NAME=orders-service \
    OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318

EXPOSE 8080
CMD ["python", "app.py"]
