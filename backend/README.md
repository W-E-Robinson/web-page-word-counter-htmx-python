# Web-page-word-counter-node

## Introduction
This repo contains a Python application that analyses a URL for both a count of the words on the page and a breakdown of word frequency. It interacts with the HTMX frontend.

## API Reference
### OPTIONS
```http
  OPTIONS /
```

### GET the HTMX reset HTML for a blank URL search form.
```http
  GET /reset
```

### GET the HTMX counts HTML (including any new, paginated or toggled displayed results)
```http
  GET /count
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `url` | `string` | **Required**. Target URL |
| `page` | `int` | Page to display |
| `display` | `bool (lowercase)` | Choose to display in depth words analysis |


## Running
### Backend
### Development mode (available at: http://localhost:8080)
```bash
pipenv install
```
```bash
pipenv run dev
```

### Docker container (container exposed on: http://localhost:8080)
```bash
docker build --pull --no-cache -t web-page-word-counter-python .
```
```bash
docker run --rm -p 8080:8080 --name web-page-word-counter-python web-page-word-counter-python
```

### Database
### Docker container (container exposed on: http://localhost:27017)
```bash
docker pull mongo:latest
```
```bash
docker run --rm --name word-counts-mongo-db -d -p 27017:27017 mongo:latest
```

## Testing
### Unit Tests
```bash
pipenv run test-unit
```

### Integration Tests
```bash
chmod +x ./run_integration_tests.sh
./run_integration_tests.sh
```
