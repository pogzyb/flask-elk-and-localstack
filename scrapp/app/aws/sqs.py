import os
import json
from structlog import get_logger

from typing import Dict, Any

from . import get_client


logger = get_logger(__name__)


def send_to_queue(item: Dict[str, Any]) -> str:
    queue_url = os.getenv('AWS_SQS_QUEUE_URL')
    client = get_client('sqs')
    response = client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(item))
    return response.get('MessageId')
