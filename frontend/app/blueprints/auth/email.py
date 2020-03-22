import logging
import os
import threading
from queue import Queue

# from flask import Flask

from app.aws_utils.ses import send_email


logger = logging.getLogger(__name__)


# TODO: define html templates for emails
# - confirm account
# - reset password
class ResetPasswordEmail:

    Subject = "Hello"
    Body = """Hi this is an email"""


# TODO: job that checks number of threads in case worker dies or maybe just sqs consumer with go?
class MailExecutor:
    """Non-blocking email manager"""

    def __init__(self):
        self._queue = Queue()
        self._num_workers = int(os.getenv('MAIL_WORKERS'))

    def init_app(self):
        self._launch_workers()

    def _launch_workers(self):
        for i in range(self._num_workers):
            ms = MailSender(name=f'mail-worker-{i+1}')
            worker = threading.Thread(target=ms.listen_for_mail, args=(self._queue,))
            worker.setDaemon(True)
            worker.start()
            logger.info(f'Launched mail-worker-{i+1}')

    def send_password_reset_email(self, email: str, token: str) -> None:
        """sends email address to queue"""
        self._queue.put(item=(email, token), block=False)
        logger.info(f'Sent {email} to email queue')


class MailSender:
    """Worker that sends email"""

    def __init__(self, name):
        self.name = name

    def listen_for_mail(self, q: Queue):
        while True:
            # todo: correctly operating email function
            logger.debug(f'{self.name} is listening')
            email, token = q.get(block=True)
            if email:
                send_email(
                    subject='Hello',
                    body='Hey you',
                    recipient=email,
                    sender='joebarzanek@gmail.com',
                    html='<h5>Whats up</h5>'
                )
                logger.debug(f'{self.name} sent email to "{email}"')
                q.task_done()


me = MailExecutor()
