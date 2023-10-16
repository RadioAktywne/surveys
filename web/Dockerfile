# hadolint ignore=DL3007
FROM ohmyform/ui:latest

USER root

RUN mkdir -p /app/ && \
    chown -R ohmyform:ohmyform /app/

WORKDIR /app/

RUN mkdir -p ./src && \
    mv /usr/src/app/ ./src/ && \
    chown -R ohmyform:ohmyform ./src/

COPY --chown=ohmyform:ohmyform ./src/ ./src/
RUN chmod +x ./src/start.sh

EXPOSE 30003

USER ohmyform

ENTRYPOINT ["./src/start.sh"]
CMD []
