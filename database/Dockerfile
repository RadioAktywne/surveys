FROM postgres:16.0-alpine3.18

WORKDIR /app/

COPY ./src/ ./src/
RUN chmod +x ./src/start.sh

COPY ./cfg/ ./cfg/

ENV DATABASE_USER=user \
    DATABASE_PASSWORD=password \
    DATABASE_NAME=database

EXPOSE 30001

ENTRYPOINT ["./src/start.sh"]
CMD []
