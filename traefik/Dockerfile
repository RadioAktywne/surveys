FROM traefik:v2.10.5

# hadolint ignore=DL3018
RUN apk add --no-cache \
    gettext-envsubst \
    moreutils

WORKDIR /app/

COPY ./src/ ./src/
RUN chmod +x ./src/start.sh

COPY ./cfg/ ./cfg/

ENV TRAEFIK_WEB_URL=http://web:30003 \
    TRAEFIK_GRAPHQL_URL=http://graphql:30004

EXPOSE 30000

ENTRYPOINT ["./src/start.sh"]
CMD []
