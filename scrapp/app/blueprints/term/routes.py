import os
from enum import Enum

from structlog import get_logger
from flask_login import login_required
from flask import (
    render_template,
    redirect,
    request,
    url_for,
    flash,
    jsonify
)

from . import term as term_router
from .schemas import term_schema
from .models import Term
from app.database import db
from app.extensions import cache
from app.search import add, search
from app.aws.kinesis import put
from app.aws.sqs import send_to_queue
from app.aws.ddb import (
    get_all_records,
    get_record,
    format_record,
    insert_record
)


logger = get_logger()


class FlashMessages:
    bad_search_form = ('Oops! Try that again.', 'danger')


@term_router.route('/scrape', methods=['POST'])
def scrape_term():
    form = dict(request.form)
    if not form.get('search-term'):
        flash(*FlashMessages.bad_search_form)
        return redirect(url_for('web.index'))

    # clear the cache on recent submissions table
    cache.delete('recent-submissions')
    # create/save the term to Postgres
    term = Term.create(term=form.get('search-term'), links=[])
    term_payload = term_schema.dump(term)
    logger.info(f'This is term payload: {term_payload}')
    put(term_payload)
    # insert term into DynamoDB # [6/30/2021] this is done by lambda
    # insert_record(item=term_payload)
    # send term off on to SQS to be further processed
    send_to_queue(item=term_payload)
    # add to elasticsearch index # [6/30/2021] this is done by lambda
    # add(os.getenv('ELASTICSEARCH_INDEX_NAME'), term)
    return redirect(url_for('web.index'))


@term_router.route('/view/<term>', methods=['GET'])
@cache.cached(timeout=30)
def view_term(term: str):
    wiki_record = get_record(term)
    term_formatted = format_record([wiki_record['Item']])
    return render_template('web/term.html', data=term_formatted)


@term_router.route('/search', methods=['GET'])
def search_term():
    term = request.args.get('term')
    if not term:
        flash(*FlashMessages.bad_search_form)
        return redirect(url_for('term.index'))
    terms = Term.from_search(os.getenv('ELASTICSEARCH_INDEX_NAME'), term, 10)
    logger.info(f'TERMS: {terms}')
    return render_template('web/search_display.html', results=terms)


@term_router.route('/recent-submissions')
@login_required
def recent_terms():
    """
    Returns most recent submissions table; caches query results for half a minute.
    """
    submissions_key = 'recent-submissions'
    if not cache.get(submissions_key):
        wiki_records = get_all_records()
        data = format_record(wiki_records['Items'])
        cache.set(submissions_key, data, timeout=30)
    else:
        data = cache.get(submissions_key)

    return jsonify(data), 200
