FROM node:20-alpine

WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev

COPY index.js .

ENV SERVICE_NAME=payments-service \
    OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318

EXPOSE 8080
CMD ["node", "index.js"]
