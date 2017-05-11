#!/usr/bin/env sh

ENVIRONMENT="$1"

RANCHER_COMPOSE_ARGS="--url ${RANCHER_URL} --access-key ${RANCHER_ACCESS_KEY} --secret-key ${RANCHER_SECRET_KEY}"
rancher-compose ${RANCHER_COMPOSE_ARGS} -p ${RANCHER_STACK} up --upgrade --force-upgrade --pull -d
rancher-compose ${RANCHER_COMPOSE_ARGS} -p ${RANCHER_STACK} up --upgrade --confirm-upgrade -d
