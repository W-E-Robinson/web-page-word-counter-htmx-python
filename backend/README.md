# web-page-word-counter-python

docker run --rm --name word-counts-mongo-db -d -p 27017:27017 mongo:latest
docker stop word-counts-mongo-db

docker build --pull --no-cache -t web-page-word-counter-python .
docker run --rm -p 8080:8080 --name web-page-word-counter-python web-page-word-counter-python
