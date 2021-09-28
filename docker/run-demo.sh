#!/bin/bash

source set-local-defs.sh
docker build --rm -t docker-nlp-python .
docker compose up
