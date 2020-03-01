import logging

import boto3

logger = logging.getLogger(__name__)


def get_client(service: str) -> boto3.client:
    # todo:
    #  1. use env vars
    #  2. check if in 'dev' or to use real aws endpoint
    if service == 'dynamodb':
        return boto3.client('dynamodb', endpoint_url='http://aws-stack:4569')
    elif service == 'sqs':
        return boto3.client('sqs', endpoint_url='http://aws-stack:4576')
    elif service == 'ses':
        return boto3.client('ses', endpoint_url='http://aws-stack:4579')
