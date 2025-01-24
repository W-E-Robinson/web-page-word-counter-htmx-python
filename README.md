# Web-page-word-counter-htmx-python

## Introduction
This repo was a job application task to create an application that analyses a URL for both a count of the words on the page and a breakdown of word frequency.
The original task required using React and Node, this repo is a recreation trying out HTMX with Python.
The repo is in two parts, the `/frontend` and `/backend`, they both contain READMEs with further information.
For instructions to run together as part of a Docker compose see below.

## Running
### Docker compose (frontend container exposed on: http://localhost:3000)
```bash
chmod +x ./build-docker-images.sh
./build-docker-images.sh && docker compose -p web-page-word-counter-htmx-python up -d
```
```bash
docker compose -p web-page-word-counter-htmx-python down -v
```
