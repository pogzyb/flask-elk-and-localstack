import logging
import time
import os

from flask_socketio import send, emit

from app import socketio
from app.aws_utils.ddb import get_record, format_record
from app.blueprints.web.web_utils import ScrapeStatus


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@socketio.event
def poll_status(term):
    logger.debug(f'Polling status for [{term}].')
    timeout = int(os.getenv('POLL_TIMEOUT', 30))
    start = time.time()
    while time.time() - start <= timeout:
        record = get_record(term)
        data = format_record([record['Item']])[0]
        if data.get('standing') == ScrapeStatus.COMPLETE:
            logger.debug(f'Finished polling; status is complete.')
            # send completed data
            emit('status', {'message': data})
            return
        logger.debug(f'Polling; status is NOT yet complete.')
        time.sleep(0.5)

    # update client on timeout error
    emit('status', {'message': ScrapeStatus.TIMEOUT})
