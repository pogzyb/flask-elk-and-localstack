#!/usr/bin/env bash

apk add jq

aws configure set aws_access_key_id 123key
aws configure set aws_secret_access_key 123secret
aws configure set aws_default_region us-east-1
aws configure set aws_region us-east-1
aws configure set aws_default_output json

export REGION=us-east-1
export DDB_TABLE_NAME=Wikis
export KIN_STREAM_NAME=wiki_app_events
export SQS_NAME=wiki_queue

# email with SES
aws --endpoint-url=http://0.0.0.0:4566 ses verify-email-identity \
    --email-address fake@email.com \
    --region ${REGION}

# create queue in SQS
aws --endpoint-url=http://0.0.0.0:4566 sqs create-queue \
    --queue-name ${SQS_NAME} \
    --region ${REGION}

# create table in DynamoDB
aws --endpoint-url=http://0.0.0.0:4566 dynamodb create-table \
    --table-name ${DDB_TABLE_NAME} \
    --cli-input-json file:///tmp/wikis.json \
    --region ${REGION} \
    --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES

export DDB_STREAM_ARN=$(aws --endpoint-url=http://0.0.0.0:4566 dynamodb describe-table --table-name ${DDB_TABLE_NAME} --region ${REGION} | jq -r '.Table.LatestStreamArn')
echo $DDB_STREAM_ARN

# create Kinesis stream
aws --endpoint-url=http://0.0.0.0:4566 kinesis create-stream \
    --stream-name ${KIN_STREAM_NAME} \
    --shard-count 3 \
    --region ${REGION}

export KIN_STREAM_ARN=$(aws --endpoint-url=http://0.0.0.0:4566 kinesis describe-stream --stream-name ${KIN_STREAM_NAME} --region ${REGION} | jq -r '.StreamDescription.StreamARN')
echo $KIN_STREAM_ARN

# create lambda function (Python3)
aws --endpoint-url=http://0.0.0.0:4566 lambda create-function \
  --function-name "py-kinesis-consumer" \
  --runtime "python3.8" \
  --handler kinesis_handler.lambda_handler \
  --memory-size 128 \
  --zip-file fileb:///tmp/lambda-files/kinesis_handler.zip \
  --role arn:aws:iam::123456:role/irrelevant \
  --region ${REGION}

# create lambda function (Python3)
#aws --endpoint-url=http://0.0.0.0:4566 lambda create-function \
#  --function-name "py-ddb-listener" \
#  --runtime "python3.8" \
#  --handler py.ddb_handler.lambda_handler \
#  --environment Variables={S3_BUCKET=Test} \
#  --memory-size 128 \
#  --zip-file fileb:///tmp/lambda-files/ddb_handler.zip \
#  --role arn:aws:iam::123456:role/irrelevant \
#  --region ${REGION}

# Go lambda
aws --endpoint-url=http://0.0.0.0:4566 lambda create-function \
  --function-name "go-ddb-listener" \
  --runtime "go1.x" \
  --handler handler \
  --environment "Variables={ELASTICSEARCH_URL=http://elasticsearch:9200,ES_INDEX_NAME=term}" \
  --memory-size 128 \
  --zip-file fileb:///tmp/lambda-files/ddb_handler.zip \
  --role arn:aws:iam::123456:role/irrelevant \
  --region ${REGION}

## register lambda functions as kinesis stream consumers
aws --endpoint-url=http://0.0.0.0:4566 lambda create-event-source-mapping \
  --function-name "py-kinesis-consumer" \
  --batch-size 5 \
  --event-source-arn ${KIN_STREAM_ARN} \
  --region ${REGION}

## register lambda function as a dynamodb stream listener
aws --endpoint-url=http://0.0.0.0:4566 lambda create-event-source-mapping \
  --function-name "go-ddb-listener" \
  --batch-size 3 \
  --event-source-arn ${DDB_STREAM_ARN} \
  --region ${REGION}

aws --endpoint-url=http://0.0.0.0:4566 --region ${REGION} logs describe-log-groups