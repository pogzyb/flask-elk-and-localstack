#!/usr/bin/env bash

go get github.com/aws/aws-lambda-go/lambda

GOOS=linux go build go/ddb_to_es/handler.go -o main

zip ddb_handler.zip main

mv ddb_handler.zip ../aws/lambda-files/ddb_handler.zip
