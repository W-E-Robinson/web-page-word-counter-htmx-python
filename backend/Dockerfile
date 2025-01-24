FROM python:3.12-slim as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

COPY Pipfile .
COPY Pipfile.lock .
COPY src/ .

EXPOSE 8080

CMD ["python3", "main.py"]
