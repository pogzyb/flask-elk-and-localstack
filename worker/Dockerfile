FROM golang:alpine3.10

RUN apk update && apk add \
    bash \
    git \
    wget \
    && apk add --no-cache openssl

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY ./worker /code
RUN chmod +x /code/start.sh

RUN go get -u github.com/aws/aws-sdk-go
RUN go get -u golang.org/x/net/html

WORKDIR /code

# todo: - localstack services will accept tcp before init-aws.sh runs in init.d
CMD ["/code/start.sh"]
