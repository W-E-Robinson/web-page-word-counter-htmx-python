#!/bin/bash

docker build --pull --no-cache -t web-page-word-counter-python .

(
  cd tests/integration
  docker-compose up -d
  sleep 5
)

pipenv run test-integration -vv

(
  cd tests/integration
  docker-compose down
)
