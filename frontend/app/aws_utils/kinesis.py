import logging
import json
import os
from typing import Dict, Any

from app.aws_utils import get_client

logger = logging.getLogger(__name__)
STREAM_NAME = os.getenv('AWS_KINESIS_STREAM_NAME')
PARTITION_KEY = os.getenv('AWS_KINESIS_PARTITION_KEY')


def put_to_stream(data: Dict[str, Any]) -> None:
    client = get_client('kinesis')
    client.put_record(
        StreamName=STREAM_NAME,
        PartitionKey=PARTITION_KEY,
        Data=json.dumps(data))
    logger.info(f'Put some data onto the kinesis stream.')
