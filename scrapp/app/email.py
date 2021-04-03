import threading
from enum import Enum
from queue import Queue
from dataclasses import dataclass

from flask import Flask, render_template
from structlog import get_logger

from app.aws.ses import send_email_with_ses


logger = get_logger(__name__)


class EmailType(str, Enum):
    REGISTRATION = 'Registration'
    PASSWORD_RESET = 'Password Reset'


@dataclass
class RegistrationEmail:
    type_: EmailType = EmailType.REGISTRATION
    sender: str = 'fake@website.com'
    subject: str = f'[{type_}] Thanks for signing up!'
    template: str = 'auth/verification_email.html'
    recipient: str = None
    token: str = None


@dataclass
class ResetPasswordEmail:
    type_: EmailType = EmailType.PASSWORD_RESET
    sender: str = 'fake@website.com'
    subject: str = f'[{type_}] Account Help'
    template: str = 'auth/reset_email.html'
    recipient: str = None
    token: str = None


class MailExecutor:
    """Launches X threads to send emails"""
    def __init__(self, app: Flask = None):
        self._app = app
        self._queue = Queue()
        if app:
            self._num_workers = int(app.config['MAIL_WORKERS'])

    def init_app(self, app: Flask):
        self._app = app
        self._num_workers = int(app.config['MAIL_WORKERS'])
        self._launch_workers()

    def _launch_workers(self):
        for i in range(self._num_workers):
            ms = MailSender(name=f'mail-thread-{i+1}', app=self._app)
            worker = threading.Thread(target=ms.listen_for_mail, args=(self._queue,))
            worker.setDaemon(True)
            worker.start()

    def send_reset_email(self, email_address: str, token: str) -> None:
        email = ResetPasswordEmail(recipient=email_address, token=token)
        self._queue.put(item=(email, None), block=False)

    def send_registration_email(self, email_address: str, token: str) -> None:
        email = RegistrationEmail(recipient=email_address, token=token)
        self._queue.put(item=(email, None), block=False)


class MailSender:
    """Mail Worker that sends application related emails"""
    def __init__(self, name: str, app: 'Flask'):
        self.name = name
        self._app_ref = app

    def listen_for_mail(self, q: Queue):
        """Listens on the queue for emails that need to be sent"""
        logger.debug(f'{self.name} is listening for email requests')
        while True:
            email, _ = q.get(block=True)
            with self._app_ref.app_context():
                html = render_template(email.template, token=email.token)
                send_email_with_ses(
                    email.subject,
                    email.sender,
                    email.recipient,
                    html)

                logger.debug(f'sent {email.type_} email to: {email.recipient}')
                q.task_done()
