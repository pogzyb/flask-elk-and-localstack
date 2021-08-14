import os
from typing import Dict, List, Any
# from threading import Lock

from structlog import get_logger

from . import get_client

logger = get_logger(__name__)


def insert_record(item: Dict[str, Any]) -> None:
    ddb = get_client('dynamodb')
    try:
        ddb.put_item(
            TableName=os.getenv('AWS_DDB_TABLE_NAME'),
            Item={
                'id': {'N': item.get('id')},
                'term': {'S': item.get('term')},
                'date_updated': {'S': item.get('date_updated')},
                'date_added': {'S': item.get('date_added')},
                'standing': {'S': 'pending'}
            }
        )
        logger.info(f'Success! Inserted item base.')
    except:
        logger.exception('could not put_item')


def get_all_records() -> Dict[str, Any]:
    ddb = get_client('dynamodb')
    response = ddb.scan(TableName=os.getenv('AWS_DDB_TABLE_NAME'))
    return response


def get_record(term: str) -> Dict[str, Any]:
    ddb = get_client('dynamodb')
    response = ddb.get_item(
        TableName=os.getenv('AWS_DDB_TABLE_NAME'),
        Key={
            'term': {
                'S': term
            }
        }
    )
    return response


def extract_from_list(links_list: List[Dict[str, Any]]) -> List[str]:
    extracted_links_list = []
    for dict_pair in links_list.get('L'):
        extracted_links_list.append(dict_pair.get('S'))
    return extracted_links_list


def extract_from_map(tags_map: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    extracted_tags_dict = {}
    for key, dict_pair in tags_map.get('M').items():
        extracted_tags_dict[key] = dict_pair.get('N')
    return extracted_tags_dict


def format_record(items_list: List[Dict[str, Dict]]) -> List[Dict[str, str]]:
    formatted_items_list = []
    for item in items_list:
        formatted_item_dict = {
            'term': item.get('term').get('S'),
            'date_updated': item.get('date_updated').get('S'),
            'date_added': item.get('date_added').get('S'),
        }
        formatted_items_list.append(formatted_item_dict)
    return formatted_items_list
