FROM python:3.12-slim
WORKDIR /app
RUN pip install flask joblib pandas scikit-learn
COPY cpu_forecast.joblib /model/cpu_forecast.joblib
COPY serve/app.py /app/app.py
EXPOSE 8080
CMD ["python","/app/app.py"]