import logging

from flask import jsonify

from app import cache
from app.blueprints.api import api
from app.aws_utils.ddb import (
    get_all_records,
    get_record,
    format_record,
    insert_record
)


logger = logging.getLogger(__name__)


@api.route('/recent-submissions')
def recent_submissions():
    """
    Returns most recent submissions table;
    Caches query results for a minute.
    """
    key = 'recent-submissions'

    if not cache.get(key):
        logger.info(f'Retrieving fresh recent-submissions')
        wiki_records = get_all_records()
        data = format_record(wiki_records['Items'])
        cache.set(key, data, timeout=15)

    else:
        logger.info(f'Retrieving cached recent-submissions')
        data = cache.get(key)

    return jsonify(data), 200
