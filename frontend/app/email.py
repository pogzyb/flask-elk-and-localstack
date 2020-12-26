import logging
import threading
from queue import Queue

from flask import render_template, Flask

from app.aws_utils.ses import send_email


logger = logging.getLogger(__name__)


class VerificationEmail:
    sender = 'fake@website.com'
    subject = 'Hello! Thanks for signing up'
    template = 'auth/verification_email.html'


class MailExecutor:
    """
    Launches X worker threads to send emails
    """
    def __init__(self, app=None):
        self._app = app
        self._num_workers = app.config['MAIL_WORKERS']
        self._queue = Queue()

    def init_app(self, app: 'Flask'):
        self._app = app.copy()
        self._launch_workers()

    def _launch_workers(self):
        for i in range(self._num_workers):
            ms = MailSender(name=f'Mail-Worker-{i+1}', app=self._app.copy())
            worker = threading.Thread(target=ms.listen_for_mail, args=(self._queue,))
            worker.setDaemon(True)
            worker.start()

    def send_password_reset_email(self, email: str, token: str) -> None:
        """
        Puts an email address on the queue
        """
        self._queue.put(item=(email, token), block=False)
        logger.info(f'Put {email} on the email queue.')


class MailSender:
    """
    Mail Worker that sends application related emails
    """
    def __init__(self, name: str, app: 'Flask'):
        self.name = name
        self._app = app

    def listen_for_mail(self, q: Queue):
        """
        Listens on `q` for emails to send

        :param q: the mail queue
        :return: None
        """
        logger.debug(f'{self.name} is listening for email requests...')
        while True:
            email_address, token = q.get(block=True)
            if email_address:
                with self._app.app_context():
                    send_email(subject=VerificationEmail.subject, sender=VerificationEmail.sender,
                               html=render_template(VerificationEmail.template, recipient=email_address, token=token))
                    logger.debug(f'{self.name} sent email to: {email_address}')
                    q.task_done()
