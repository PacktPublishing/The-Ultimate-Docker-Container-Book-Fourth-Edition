FROM golang:1.23 AS builder
WORKDIR /app

# Disable modules so no go.mod is needed
ENV GO111MODULE=off
COPY main.go .
RUN CGO_ENABLED=0 GOOS=linux \
    go build -ldflags="-s -w" -o hello

FROM scratch
COPY --from=builder /app/hello /hello
ENTRYPOINT ["/hello"]
