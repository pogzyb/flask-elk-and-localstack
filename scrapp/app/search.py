import datetime
from typing import List, Tuple, Dict, Any

from structlog import get_logger
from flask import current_app
from flask_sqlalchemy.model import Model


logger = get_logger(__name__)


def add(index_name: str, model_obj: Model):
    """
    Adds the model_obj's searchable fields to `index_name` in Elasticsearch.

    :param index_name: name of existing index in elasticsearch
    :param model_obj: the model object to add
    :return: None
    """
    es = current_app.elasticsearch
    payload = {}
    for field in model_obj.__searchable__:
        value = getattr(model_obj, field)
        if isinstance(value, datetime.datetime):
            value = value.isoformat()
        payload[field] = value
    es.index(index=index_name, id=model_obj.id, body=payload)


def delete(index_name: str, obj_id: int):
    """

    :param index_name:
    :param obj_id:
    :return:
    """
    es = current_app.elasticsearch
    es.delete(index=index_name, id=obj_id)
    return


def search(index_name: str, term: str, size: int) -> Tuple[List[int], int]:
    """

    :param index_name:
    :param term:
    :param size:
    :return:
    """
    es = current_app.elasticsearch
    results = es.search(
        index=index_name,
        body={'query': {'multi_match': {'query': term, 'fields': ['*']}}})
    logger.info(f'RESULTS: {results}')
    total = results['hits']['total']['value']
    ids = [doc['_id'] for doc in results['hits']['hits']]
    return ids, total
