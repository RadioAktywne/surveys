#!/bin/sh

DB_USER="${GRAPHQL_DATABASE_USER:-user}"
DB_PASSWORD="${GRAPHQL_DATABASE_PASSWORD:-password}"
DB_HOST="${GRAPHQL_DATABASE_HOST:-database}"
DB_PORT="${GRAPHQL_DATABASE_PORT:-30001}"
DB_NAME="${GRAPHQL_DATABASE_NAME:-database}"

DB_URL="postgres://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

DATABASE_DRIVER=postgres \
	DATABASE_URL="${DB_URL}" \
	REDIS_HOST="${GRAPHQL_REDIS_HOST:-redis}" \
	REDIS_PORT="${GRAPHQL_REDIS_PORT:-30002}" \
	CREATE_ADMIN=1 \
	ADMIN_USERNAME="${GRAPHQL_ADMIN_USER:-admin}" \
	ADMIN_PASSWORD="${GRAPHQL_ADMIN_PASSWORD:-password}" \
	ADMIN_EMAIL="${GRAPHQL_ADMIN_EMAIL:-'it@radioaktywne.pl'}" \
	DISABLE_INSTALLATION_METRICS=1 \
	SECRET_KEY="${GRAPHQL_SECRET_KEY:-secret}" \
	HIDE_CONTRIB=1 \
	SIGNUP_DISABLED=1 \
	BASE_URL="${GRAPHQL_WEB_PUBLIC_URL:-'http://localhost:30000'}" \
	PORT=30004 \
	\
	docker-entrypoint.sh \
	yarn \
	--cwd ./src/app/ \
	start:prod