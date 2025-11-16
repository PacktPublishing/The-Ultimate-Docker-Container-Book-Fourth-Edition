FROM python:3.12-slim
WORKDIR /app
COPY app/train.py /app/train.py
RUN pip install --no-cache-dir pandas scikit-learn joblib
CMD ["python", "/app/train.py"]