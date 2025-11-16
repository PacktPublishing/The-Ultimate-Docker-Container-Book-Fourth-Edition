FROM golang:1.23-alpine AS build
WORKDIR /src
COPY . .
RUN go mod init go-service && go mod tidy && \
    go build -o app

FROM alpine
WORKDIR /app
COPY --from=build /src/app .
EXPOSE 8081
CMD ["./app"]
