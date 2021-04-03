from functools import lru_cache

from structlog import get_logger
import boto3


logger = get_logger(__name__)


@lru_cache
def get_session():
    logger.debug(f'creating boto3 session')
    return boto3.session.Session()


def get_client(service: str) -> boto3.client:
    sess = get_session()
    logger.debug(f'creating {service} client')
    return sess.client(service, endpoint_url='http://aws-stack:4566')
