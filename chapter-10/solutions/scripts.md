# Scripts for Chapter 10
Run the catalog service with appropriate Traefik labels
```
docker container run --rm -d \
    --name catalog \
    --label traefik.enable=true \
    --label traefik.port=3000 \
    --label traefik.priority=10 \
    --label traefik.http.routers.catalog.rule="Host(\"acme.com\") && PathPrefix(\"/catalog\")" \
    acme/catalog:1.0
````

Run the city-tours service with appropriate Traefik labels
```
docker container run --rm -d \
    --name city-tours \
    --label traefik.enable=true \
    --label traefik.port=5000 \
    --label traefik.priority=1 \
    --label traefik.http.routers.city-tours.rule="Host(\"acme.com\")" \
    acme/city-tours:1.0
```

Run Traefik with Docker provider and dashboard enabled
```
docker run -d \
    --name traefik \
    -p 8080:8080 \
    -p 80:80 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    traefik:v2.0 \
        --api.insecure=true \
        --providers.docker=true \
        --entrypoints.web.address=:80 \
        --log.level=DEBUG \
        --providers.docker.exposedbydefault=false
```

Test the setup by querying the catalog service through Traefik
Option 1: Assuming you are able to resolve acme.com via /etc/hosts
```
curl -sL http://acme.com/catalog/tours?city=paris | jq .
```

Option 2: Using --resolve to map acme.com to localhost, if you cannot modify /etc/hosts
```
curl -sL --resolve acme.com:80:127.0.0.1 "http://acme.com/catalog/tours?city=paris" | jq .
```