FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html

# NGINX runs as root by default in many images; 
# switch to a high UID
RUN adduser -D -u 10100 web && chown -R web:web \
    /var/cache/nginx \
    /var/run \
    /var/log/nginx \
    /usr/share/nginx/html
USER 10100

EXPOSE 80