FROM alpine:3.20
RUN apk add --no-cache bash curl wget ca-certificates && \
    curl -LO "https://dl.k8s.io/release/v1.30.2/bin/linux/amd64/kubectl" && \
    install -m 0755 kubectl /usr/local/bin/kubectl && rm kubectl
COPY run-scaler.sh /usr/local/bin/run-scaler.sh
RUN chmod +x /usr/local/bin/run-scaler.sh
ENTRYPOINT ["/usr/local/bin/run-scaler.sh"]