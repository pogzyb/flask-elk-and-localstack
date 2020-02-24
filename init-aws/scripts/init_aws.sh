#!/usr/bin/env bash

aws configure set aws_access_key_id 123key
aws configure set aws_secret_access_key 123secret
aws configure set aws_default_region us-east-1
aws configure set aws_default_output json

# create a queue in SQS
aws --endpoint-url=http://0.0.0.0:4576 sqs create-queue \
    --queue-name wikis \
    --region us-east-1

# create a table in DynamoDB
aws --endpoint-url=http://0.0.0.0:4569 dynamodb create-table \
    --table-name Wikis \
    --cli-input-json file:///tmp/wikis.json \
    --region us-east-1


