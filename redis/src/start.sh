#!/bin/sh

docker-entrypoint.sh \
	redis-server \
	./cfg/redis.conf
