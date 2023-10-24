#!/bin/bash

# Activate runtime shell
# shellcheck source=/dev/null
. /env/activate

# Activate virtual environment
# shellcheck source=/dev/null
. .venv/bin/activate

# Run as non-root user
# Use tini to handle signals
API__GRAPHQL__HOST="${API_GRAPHQL_HOST:-graphql}" \
	API__GRAPHQL__PORT="${API_GRAPHQL_PORT:-30004}" \
	API__GRAPHQL__USER="${API_GRAPHQL_USER:-admin}" \
	API__GRAPHQL__PASSWORD="${API_GRAPHQL_PASSWORD:-password}" \
	\
	su-exec \
	app \
	tini \
	-s \
	-- \
	"$@"
