FROM bitnami/kubectl:latest

USER root

COPY scale.sh /scripts/scale.sh
RUN chmod +x /scripts/scale.sh

USER 1001

ENTRYPOINT ["bash", "/scripts/scale.sh"]
