# Production-ready Dockerfile for Node.js Express app
# Use official Node.js LTS image as base
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci --only=production || npm install --only=production

# Copy app source
COPY index.js ./

# Use a minimal image for the final stage
FROM node:20-alpine
WORKDIR /app

# Copy only the necessary files from builder
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/index.js ./
COPY --from=builder /app/package.json ./
COPY entrypoint.sh ./

# Make entrypoint.sh executable
RUN chmod +x ./entrypoint.sh

# Expose the port
EXPOSE 3000

# Use entrypoint.sh as entrypoint
ENTRYPOINT ["./entrypoint.sh"]
