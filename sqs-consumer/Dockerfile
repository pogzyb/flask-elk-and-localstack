# compile stage
FROM golang:alpine3.11 as compile

COPY ./sqs-consumer /go/src/pogzyb/

WORKDIR /go/src/pogzyb/

RUN apk add git
RUN go get -v ./...
RUN GOARCH=amd64 GOOS=linux go build -o consume .

# complete stage
FROM alpine:3.11

RUN apk update && apk add --no-cache \
    bash \
    wget \
    openssl

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY ./sqs-consumer/start.sh /code/start.sh

RUN chmod +x /code/start.sh
COPY --from=compile /go/src/pogzyb/consume /code/consume

CMD ["/code/start.sh"]
