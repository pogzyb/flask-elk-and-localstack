import logging
from functools import lru_cache

import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@lru_cache
def get_session():
    logger.debug(f'creating boto3 session')
    return boto3.session.Session()


def get_client(service: str) -> boto3.client:
    sess = get_session()
    logger.debug(f'creating {service} client')
    return sess.client(service, endpoint_url='http://aws-stack:4566')
