#!/usr/bin/env bash

go get github.com/aws/aws-lambda-go/lambda

cd ddb_to_es

GOOS=linux go build handler.go

zip ddb_handler.zip handler

mv ddb_handler.zip ../../../aws/lambda-files/ddb_handler.zip
