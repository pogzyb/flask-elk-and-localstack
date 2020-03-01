FROM python:3.8-alpine

COPY ./frontend/requirements.txt /tmp/requirements.txt

RUN apk update && apk add \
    build-base \
    linux-headers \
    pcre-dev \
    bash \
    && apk add --virtual build-deps \
    gcc \
    python-dev \
    musl-dev \
    && apk add --no-cache openssl \
    && apk add postgresql-dev \
    && pip install -r /tmp/requirements.txt

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY ./frontend/entrypoint.sh /entrypoint.sh
COPY ./frontend /code
WORKDIR /code

EXPOSE ${APP_PORT}
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]