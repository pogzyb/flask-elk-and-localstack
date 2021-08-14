from dataclasses import dataclass
from typing import List

from structlog import get_logger
import redis


logger = get_logger(__name__)


@dataclass
class TokenData:
    uuid: str
    user_id: int
    user_roles: List[str]


def put_token(uuid: str, data: TokenData):

    return


def pop_token(uuid: str):

    return


def get_token(uuid: str):
    return
