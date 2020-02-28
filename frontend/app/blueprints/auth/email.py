import logging
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from flask import Flask

from app.utils.ses import send_mail


logger = logging.getLogger(__name__)


class MailExecutor:
    """Non-blocking email manager"""

    def __init__(self, app: Flask = None, mail: Mail = None):
        self._queue = Queue()
        self._executor = ThreadPoolExecutor(max_workers=2)
        self._app = app
        self._mail = mail

    def init_app(self, app: Flask, mail: Mail):
        self._app = app
        self._mail = mail
        self._launch_workers()
        self._queue.join()

    def _launch_workers(self):
        for i in range(2):
            ms = MailSender(name=f'mail-worker-{i+1}')
            self._executor.submit(ms.listen_for_mail, args=(self._queue, self._app, self._mail))
            logger.info(f'Launched mail-worker-{i+1}')

    def send_password_reset_email(self, email: str) -> None:
        """sends email address to queue"""
        self._queue.put(item=email, block=True, timeout=10)
        logger.info(f'Sent {email} to email queue')


class MailSender:
    """Worker that sends email"""

    def __init__(self, name):
        self.name = name

    def listen_for_mail(self, email_queue: Queue, app: Flask, mail: Mail):
        logger.info(f'{self.name} is listening!')
        while True:
            email = email_queue.get()
            if email:
                with app.app_context():
                    msg = Message("A message!", sender="joe ", recipients=["joebarzanek@gmail.com"])
                    msg.body = "Hey!!"
                    msg.html = "<h2>HI</h2>"
                    mail.send(msg)
                email_queue.task_done()


me = MailExecutor()
