FROM python:3.8-alpine

ENV APP_LOGS_DIR=/logs
ENV APP_HOME=/scrapp
ENV HOME=${APP_HOME}
COPY ./scrapp/requirements.txt /tmp/requirements.txt

RUN apk update && apk add \
    build-base \
    linux-headers \
    pcre-dev \
    bash \
    && apk add --virtual build-deps \
    gcc \
    libffi-dev \
    python3-dev \
    musl-dev \
    py3-gevent \
    && apk add --no-cache openssl \
    && apk add postgresql-dev \
    && pip3 install -r /tmp/requirements.txt \
    && apk del build-deps

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY ./scrapp ${APP_HOME}
COPY ./scrapp/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN mkdir -p ${APP_LOGS_DIR}
WORKDIR ${APP_HOME}

EXPOSE ${APP_PORT}
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]