# web-page-word-counter-frontend-htmx

## Introduction
This is a HTMX frontend that allows the user to input a web page URL and receive both a count of the words on the page as well as a breakdown of word frequency.

## Development
### Serve files through local server (below or equivalent)
```sh
python3 -m http.server 3000
```

### Docker container (container exposed on: http://localhost:3000)
```bash
docker build --pull --no-cache -t web-page-word-counter-htmx .
```
```bash
docker run --rm -p 3000:3000 --name web-page-word-counter-htmx web-page-word-counter-htmx
```
