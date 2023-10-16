#!/bin/sh

PORT=30003 \
	\
	docker-entrypoint.sh \
	yarn \
	--cwd ./src/app/ \
	start
