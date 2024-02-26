FROM python:3.11

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN apt-get update
RUN python3 -m venv .venv && \
    . .venv/bin/activate && \
    pip install poetry==1.8.0

RUN .venv/bin/poetry config virtualenvs.create false

RUN .venv/bin/poetry install
CMD [".venv/bin/poetry", "run", "python", "metrics_collector/cli.py"]