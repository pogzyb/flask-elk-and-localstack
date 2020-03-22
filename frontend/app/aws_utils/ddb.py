import logging
from typing import Dict, List, Any

from app.aws_utils.api import get_client

logger = logging.getLogger(__name__)


def insert_record(item: Dict[str, Any]) -> None:
    ddb = get_client('dynamodb')
    try:
        ddb.put_item(
            TableName='Wikis',
            Item={
                'name': {'S': item.get('name')},
                'timestamp': {'S': item.get('timestamp')},
                'standing': {'S': item.get('standing')},
                'links': {'L': item.get('links')},
                'tags': {'M': item.get('tags')}
            }
        )
        logger.info(f'Success! Inserted item base.')
    except Exception as e:
        logger.exception(e)


def get_all_records() -> Dict[str, Any]:
    ddb = get_client('dynamodb')
    response = ddb.scan(TableName='Wikis')
    # logger.info(f'{response}')
    return response


def get_single_record(term: str) -> Dict[str, Any]:
    ddb = get_client('dynamodb')
    response = ddb.get_item(
        TableName='Wikis',
        Key={
            'name': {
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


def format_query_result(items_list: List[Dict[str, Dict]]) -> List[Dict[str, str]]:
    formatted_items_list = []
    for item in items_list:
        formatted_item_dict = {
            'name': item.get('name').get('S'),
            'standing': item.get('standing').get('S'),
            'timestamp': item.get('timestamp').get('S'),
            'links': extract_from_list(item.get('links')),
            'tags': extract_from_map(item.get('tags'))
        }
        formatted_items_list.append(formatted_item_dict)
    return formatted_items_list
