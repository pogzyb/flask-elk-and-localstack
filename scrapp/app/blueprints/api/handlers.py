from flask import jsonify
from flask_login import login_required
from structlog import get_logger

from app import cache
from app.blueprints.api import api
from app.aws.ddb import (
    get_all_records,
    get_record,
    format_record,
    insert_record
)


logger = get_logger(__name__)


@api.route('/recent-submissions')
@login_required
def recent_submissions():
    """
    Returns most recent submissions table;
    Caches query results for a minute.
    """
    key = 'recent-submissions'
    if not cache.get(key):
        logger.info(f'retrieving fresh recent-submissions')
        wiki_records = get_all_records()
        data = format_record(wiki_records['Items'])
        cache.set(key, data, timeout=15)

    else:
        logger.info(f'retrieving cached recent-submissions')
        data = cache.get(key)

    return jsonify(data), 200
