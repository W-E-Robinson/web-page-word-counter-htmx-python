FROM python:3.9-slim

WORKDIR /app

COPY index.html .
COPY index.css .

EXPOSE 3000

CMD ["python3", "-m", "http.server", "8000"]
