FROM node:20-alpine
WORKDIR /app
COPY server.js entrypoint.sh ./
RUN npm install express && chmod +x entrypoint.sh
EXPOSE 8080
CMD ["./entrypoint.sh"]
