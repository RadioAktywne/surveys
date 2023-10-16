#!/bin/sh

POSTGRES_USER="${DATABASE_USER:-user}" \
	POSTGRES_PASSWORD="${DATABASE_PASSWORD:-password}" \
	POSTGRES_DB="${DATABASE_NAME:-database}" \
	PGDATA=./data/ \
	\
	docker-entrypoint.sh \
	postgres \
	-c config_file=./cfg/postgres.conf
