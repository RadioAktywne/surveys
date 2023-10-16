FROM redis:7.2.1-alpine3.18

WORKDIR /app/

COPY ./src/ ./src/
RUN chmod +x ./src/start.sh

COPY ./cfg/ ./cfg/

EXPOSE 30002

ENTRYPOINT ["./src/start.sh"]
CMD []
