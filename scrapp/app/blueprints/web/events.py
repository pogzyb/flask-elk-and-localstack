# import time
# import os
#
# from flask_socketio import send, emit
# from structlog import get_logger
#
# from .web_utils import ScrapeStatus
# from app import socketio
# from app.aws.ddb import get_record, format_record
#
#
# logger = get_logger(__name__)
#
#
# @socketio.event  # Uses SocketIO to keep a connection open to the client.
# def poll_status(term: str):
#     """
#     Queries DynamoDB for "term" every second and checks its status;
#     returns once the status is "complete" or the timeout has been
#     reached.
#
#     :param term: the term that was submitted for "scraping"
#     :return:
#     """
#     logger.info(f'started polling status for: {term}')
#     timeout = int(os.getenv('POLL_TIMEOUT', 30))
#     start = time.time()
#     while time.time() - start <= timeout:
#         record = get_record(term)
#         data = format_record([record['Item']])[0]
#         if data.get('standing') == ScrapeStatus.COMPLETE:
#             logger.info(f'finished polling; status is complete')
#             # send completed data; right now it's just a simple status message
#             emit('status', {'message': data})
#             return
#         # wait
#         time.sleep(1.0)
#
#     # update client on timeout error
#     emit('status', {'message': ScrapeStatus.TIMEOUT})
