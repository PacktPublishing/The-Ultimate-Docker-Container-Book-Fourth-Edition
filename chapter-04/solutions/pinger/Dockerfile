FROM alpine:3.21
RUN apk update && apk add curl
ENTRYPOINT ["ping"]
CMD ["-c","3","8.8.8.8"]
