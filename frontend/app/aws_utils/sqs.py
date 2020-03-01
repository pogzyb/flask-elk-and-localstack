import os
import json
import logging
from typing import Dict, Any

from app.aws_utils.api import get_client

logger = logging.getLogger(__name__)


def send_to_queue(item: Dict[str, Any]) -> str:
    queue_url = os.getenv('AWS_SQS_QUEUE_URL')
    client = get_client('sqs')
    response = client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(item))
    return response.get('MessageId')
