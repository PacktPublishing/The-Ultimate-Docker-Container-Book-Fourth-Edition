FROM ruby:3.3-alpine
WORKDIR /app
COPY worker.rb entrypoint.sh ./
RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]