#!/usr/bin/env bash

apk add jq

aws configure set aws_access_key_id 123key
aws configure set aws_secret_access_key 123secret
aws configure set aws_default_region us-east-1
aws configure set aws_region us-east-1
aws configure set aws_default_output json

export REGION=us-east-1
export STREAM_NAME=logs

# email with SES
aws --endpoint-url=http://0.0.0.0:4566 ses verify-email-identity \
    --email-address fake@email.com \
    --region ${REGION}

# create queue in SQS
aws --endpoint-url=http://0.0.0.0:4566 sqs create-queue \
    --queue-name wikis \
    --region ${REGION}

# create table in DynamoDB
aws --endpoint-url=http://0.0.0.0:4566 dynamodb create-table \
    --table-name Wikis \
    --cli-input-json file:///tmp/wikis.json \
    --region ${REGION}

# create kinesis stream
aws --endpoint-url=http://0.0.0.0:4566 kinesis create-stream \
    --stream-name ${STREAM_NAME} \
    --shard-count 3 \
    --region ${REGION}

export STREAM_ARN=$(aws --endpoint-url=http://0.0.0.0:4566 kinesis describe-stream --stream-name ${STREAM_NAME} --region ${REGION} | jq '.StreamDescription.StreamARN')


# create lambda function (Python3)
aws --endpoint-url=http://0.0.0.0:4566 lambda create-function \
  --function-name "py-stream-consumer" \
  --runtime "python3.8" \
  --handler py.consumer.lambda_handler \
  --memory-size 128 \
  --zip-file fileb:///tmp/lambda-files/py-handler.zip \
  --role arn:aws:iam::123456:role/irrelevant \
  --region ${REGION}

## TODO: create lambda function (Go)
#
## register lambda functions as kinesis stream consumers
aws --endpoint-url=http://0.0.0.0:4566 lambda create-event-source-mapping \
  --function-name "py-stream-consumer" \
  --batch-size 5 \
  --event-source-arn arn:aws:kinesis:us-east-1:000000000000:stream/logs \
  --region ${REGION}