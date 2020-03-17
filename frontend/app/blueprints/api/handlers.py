import logging

from flask import jsonify, request

from app import cache
from app.blueprints.api import api
from app.aws_utils.ddb import (
    get_all_records,
    get_single_record,
    format_query_result,
    insert_record
)


logger = logging.getLogger(__name__)


@api.route('/recent-submissions-table')
@cache.cached(timeout=60)
def recent_submissions_table():
    """Returns most recent submissions"""
    wiki_records = get_all_records()
    data = format_query_result(wiki_records['Items'])
    return jsonify(data), 200
