FROM python:3.12

WORKDIR /app

COPY ./server/pyproject.toml ./server/poetry.lock* /app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY ./server /app

CMD ["tail", "-f", "/dev/null"]
