from datetime import datetime

from structlog import get_logger
from flask_login import current_user
from flask import (
    render_template,
    redirect,
    request,
    url_for,
    flash
)

from . import web
from .web_utils import FlashMessages, ScrapeStatus
from app.extensions import cache
from app.aws.sqs import send_to_queue
from app.aws.ddb import get_all_records, get_record, format_record, insert_record
from app.aws.kinesis import put_to_stream


logger = get_logger()


@web.route('/', methods=['GET'])
def index():
    logger.info(f'{current_user.email if current_user.is_authenticated else "anonymous"} is viewing the home page')
    return render_template('web/index.html', current_user=current_user)


@web.route('/scrape', methods=['POST'])
def scrape_term():
    form = dict(request.form)
    kinesis_payload = {
        'src_ip': request.remote_addr,
        'path': request.url,
        'timestamp': datetime.utcnow().isoformat(),
        'search_term': form.get('search-term') or ''
    }
    put_to_stream(kinesis_payload)
    if not form.get('search-term'):
        flash(*FlashMessages.bad_search_form)
        return redirect(url_for('web.index'))
    # clear the cache on recent submissions table
    cache.delete('recent-submissions')
    payload = {
        'name': form.get('search-term'),
        'timestamp': datetime.utcnow().isoformat(),
        'standing': ScrapeStatus.PENDING,
        'links': [],
        'tags': {}
    }
    # insert the record into dynamodb
    insert_record(item=payload)
    # send the payload off on sqs to be further processed
    send_to_queue(item=payload)

    return redirect(url_for('web.index'))


@web.route('/view/<term>', methods=['GET'])
@cache.cached(timeout=30)
def view_term(term: str):
    logger.info(f'viewing term {term}')
    wiki_record = get_record(term)
    data = format_record([wiki_record['Item']])
    return render_template('web/term.html', data=data, current_user=current_user)
