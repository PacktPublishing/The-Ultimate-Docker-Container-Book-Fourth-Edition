FROM node:18-alpine
WORKDIR /app

# Install curl for health check
RUN apk add --no-cache curl

COPY package*.json ./
RUN npm install --only=production
COPY . .
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Start the application
CMD ["npm", "start"]
