#!/bin/sh

envsubst <./cfg/static.yaml | sponge ./cfg/static.yaml
envsubst <./cfg/dynamic.yaml | sponge ./cfg/dynamic.yaml

/entrypoint.sh traefik --configFile=./cfg/static.yaml
