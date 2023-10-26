FROM traefik:v2.10.5

# hadolint ignore=DL3018
RUN apk add --no-cache \
    gettext-envsubst \
    moreutils

WORKDIR /app/

COPY ./src/ ./src/
RUN chmod +x ./src/start.sh

COPY ./cfg/ ./cfg/

ENV TRAEFIK_API_HOST=localhost \
    TRAEFIK_API_PORT=30005 \
    TRAEFIK_GRAPHQL_HOST=localhost \
    TRAEFIK_GRAPHQL_PORT=30004 \
    TRAEFIK_WEB_HOST=localhost \
    TRAEFIK_WEB_PORT=30003

EXPOSE 30000

ENTRYPOINT ["./src/start.sh"]
CMD []
