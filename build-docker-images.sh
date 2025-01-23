#!/bin/bash
docker build --pull --no-cache -t web-page-word-counter-htmx -f frontend/Dockerfile frontend/
docker build --pull --no-cache -t web-page-word-counter-python -f backend/Dockerfile backend/
docker pull mongo:latest
