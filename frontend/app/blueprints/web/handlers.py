import logging
from datetime import datetime
import json
import time

from flask_login import current_user
from flask_socketio import send, emit
from flask import (
    Blueprint,
    jsonify,
    render_template,
    redirect,
    request,
    url_for
)

from app import socketio
from app.blueprints.web import web
from app.aws_utils.sqs import send_to_queue
from app.aws_utils.ddb import (
    get_all_records,
    get_single_record,
    format_query_result,
    insert_record
)


logger = logging.getLogger(__name__)


@web.route('/', methods=['GET'])
def index():
    return render_template('web/index.html', current_user=current_user)


@web.route('/scrape', methods=['POST'])
def scrape_term():
    form = dict(request.form)
    if not form.get('search-term'):
        return redirect('/')
    payload = {
        'name': form.get('search-term'),
        'timestamp': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        'standing': 'pending',
        'links': []
    }
    insert_record(item=payload)
    send_to_queue(item=payload)
    return redirect(url_for('web.view_term', term=form.get('search-term')))


@web.route('/view/<term>', methods=['GET'])
def view_term(term: str):
    wiki_record = get_single_record(term)
    data = format_query_result([wiki_record['Item']])
    return render_template('web/term.html', data=data)


@socketio.on('view-page')
def page_socket(term: str):
    logger.info(f'Checking status for {term}...')
    while True:
        record = get_single_record(term)
        data = format_query_result([record['Item']])[0]
        if data.get('standing') == 'complete':
            logger.info(f'Complete!: {data}')
            break
        time.sleep(1)

    emit('status', {'message': data})
