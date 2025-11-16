FROM alpine:3.21.3
# Install curl & jq
RUN apk --no-cache add curl jq
WORKDIR /app
COPY trivia.sh ./
RUN chmod +x trivia.sh
CMD ["./trivia.sh"]