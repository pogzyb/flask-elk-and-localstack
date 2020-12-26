import logging
import threading
from queue import Queue

from flask import (
    Flask,
    render_template,
    copy_current_request_context
)

from app.aws_utils.ses import send_email_with_ses


logger = logging.getLogger(__name__)


def copy_current_app_context(func):

    def wrapper(*args, **kwargs):
        return

    return


class VerificationEmail:
    sender = 'fake@website.com'
    subject = 'Hello! Thanks for signing up'
    template = 'auth/verification_email.html'


class ResetPasswordEmail:
    sender = 'fake@website.com'
    subject = 'Account Recovery Information'
    template = 'auth/reset_password_email.html'


class MailExecutor:
    """
    Launches X sqs-consumer threads to send emails
    """
    def __init__(self, app=None):
        self._app = app
        self._queue = Queue()
        if app:
            self._num_workers = int(app.config['MAIL_WORKERS'])

    def init_app(self, app: 'Flask'):
        self._app = app
        self._num_workers = int(app.config['MAIL_WORKERS'])
        self._launch_workers()

    def _launch_workers(self):
        for i in range(self._num_workers):
            ms = MailSender(name=f'Mail-Worker-{i+1}', app=self._app)
            worker = threading.Thread(target=ms.listen_for_mail, args=(self._queue,))
            worker.setDaemon(True)
            worker.start()

    def send_password_reset_email(self, email_address: str, token: str) -> None:
        """
        Puts an email address on the queue
        """
        self._queue.put(item=(email_address, token, 'reset'), block=False)
        logger.info(f'Put {email_address} on the email queue.')

    def send_verification_email(self, email_address: str, token: str) -> None:
        """

        :param email_address:
        :param token:
        :return:
        """
        self._queue.put(item=(email_address, token, 'verify'), block=False)


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
            email_address, token, kind = q.get(block=True)
            if kind == "verify":
                email = VerificationEmail()
            elif kind == "reset":
                email = ResetPasswordEmail()
            else:
                logger.debug(f'email kind: [{kind}] is not recognized.')
                continue

            with self._app.app_context():
                # invoke SES to send the email
                send_email_with_ses(subject=email.subject, sender=email.sender, recipient=email_address,
                                    html=render_template(email.template, token=token))

                logger.debug(f'{self.name} sent email to: {email_address}')
                q.task_done()
