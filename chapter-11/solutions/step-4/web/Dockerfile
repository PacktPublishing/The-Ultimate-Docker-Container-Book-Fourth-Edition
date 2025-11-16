FROM node:20-alpine AS build
# Set working directory
WORKDIR /app
# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev || npm install --omit=dev
# Copy app source
COPY . .
# Expose the port the app runs on
EXPOSE 3000
# Use a non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
# Start the app
CMD ["npm", "start"]
