# hadolint ignore=DL3007
FROM ohmyform/api:latest

USER root

RUN mkdir -p /app/ && \
    chown -R ohmyform:ohmyform /app/

WORKDIR /app/

RUN mkdir -p ./src && \
    mv /usr/src/app/ ./src/ && \
    chown -R ohmyform:ohmyform ./src/

COPY --chown=ohmyform:ohmyform ./src/ ./src/
RUN chmod +x ./src/start.sh

ENV GRAPHQL_DATABASE_USER=user \
    GRAPHQL_DATABASE_PASSWORD=password \
    GRAPHQL_DATABASE_HOST=database \
    GRAPHQL_DATABASE_PORT=30001 \
    GRAPHQL_DATABASE_NAME=database \
    GRAPHQL_REDIS_HOST=redis \
    GRAPHQL_REDIS_PORT=30002 \
    GRAPHQL_ADMIN_USER=admin \
    GRAPHQL_ADMIN_PASSWORD=password \
    GRAPHQL_ADMIN_EMAIL=it@radioaktywne.pl \
    GRAPHQL_SECRET_KEY=secret \
    GRAPHQL_WEB_PUBLIC_URL=http://localhost:30000

EXPOSE 30004

USER ohmyform

ENTRYPOINT ["./src/start.sh"]
CMD []
