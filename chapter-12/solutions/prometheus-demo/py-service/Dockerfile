FROM python:3.12-slim
WORKDIR /app
COPY app.py .
RUN pip install flask prometheus_client
EXPOSE 8082
CMD ["python", "app.py"]
