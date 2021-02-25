FROM python:3.9-slim-buster

LABEL org.opencontainers.image.source="https://github.com/thunderstore-io/thunderstore-discord-bot"

WORKDIR /app


COPY ./pyproject.toml ./poetry.lock ./main.py /app/

RUN pip install -U pip poetry~=1.1.4 --no-cache-dir && \
    poetry config virtualenvs.create false && \
    poetry install && \
    rm -rf ~/.cache

COPY ./thunderbot /app/thunderbot

ENTRYPOINT ["python", "/app/main.py"]