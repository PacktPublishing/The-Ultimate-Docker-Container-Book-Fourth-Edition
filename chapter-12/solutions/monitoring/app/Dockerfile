FROM node:20-alpine
WORKDIR /usr/src/app
COPY server.js .
RUN npm install express prom-client
EXPOSE 8080
CMD ["node", "server.js"]
