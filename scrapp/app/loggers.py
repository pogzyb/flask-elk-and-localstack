import os
import logging

import structlog
from gunicorn import glogging
from flask import has_request_context, request


class LoggerConfig:

    class RequestFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            if has_request_context():
                record.src_ip = request.remote_addr

            return super().format(record)

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def add_access_log_info(_, __, event_dict):
        """
        https://albersdevelopment.net/2019/08/15/using-structlog-with-gunicorn/
        """
        if event_dict.get('logger') == 'geventwebsocket.handler':
            message = event_dict['event']
            # 172.25.0.1 - - [2021-03-28 15:53:35] \"GET / HTTP/1.1\" 200 4178 0.042716
            # event_dict

        return event_dict

    @property
    def preprocessor_chain(self):
        # https://www.structlog.org/en/stable/standard-library.html#rendering-using-structlog-based-formatters-within-logging
        pre_chain_funcs = [
            structlog.processors.TimeStamper(),
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            self.add_access_log_info,
        ]
        return pre_chain_funcs

    @property
    def dict_config(self):
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'json': {
                    '()': structlog.stdlib.ProcessorFormatter,
                    'processor': structlog.processors.JSONRenderer(),
                    'foreign_pre_chain': self.preprocessor_chain,
                },
                'console': {
                    '()': structlog.stdlib.ProcessorFormatter,
                    'processor': structlog.dev.ConsoleRenderer(colors=True),
                    'foreign_pre_chain': self.preprocessor_chain,
                }
            },
            'handlers': {
                'json_file': {
                    'level': 'INFO',
                    'formatter': 'json',
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'filename': os.path.join(os.getenv('APP_LOGS_DIR'), os.getenv('APP_LOG_FILENAME')),
                    'utc': True,
                    'when': 'midnight'
                },
                'default': {
                    'level': 'INFO',
                    'formatter': 'console',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout'
                },
            },
            'loggers': {
                '': {  # root logger
                    'handlers': ['default', 'json_file'],
                    'level': 'INFO',
                    'propagate': True,
                },
                'geventwebsocket.handler': {
                    'handlers': ['default', 'json_file'],
                    'level': 'INFO',
                    'propagate': True,
                },
                'gunicorn.access': {
                    'handlers': ['default', 'json_file'],
                    'level': 'INFO',
                    'propagate': True,
                },
                'gunicorn.error': {
                    'handlers': ['default', 'json_file'],
                    'level': 'INFO',
                    'propagate': True,
                },
            }
        }


class GunicornLogger(glogging.Logger):
    """
    https://github.com/benoitc/gunicorn/blob/master/gunicorn/glogging.py
    """
    def __init__(self, cfg):
        super().__init__(cfg)
        self.access_log = structlog.get_logger('gunicorn.access')
        self.access_log.setLevel(logging.INFO)
        self.error_log = structlog.get_logger('gunicorn.error')
        self.error_log.setLevel(logging.INFO)
        self.cfg = cfg

    def log_request(self):
        if '101' not in str(self.status):
            self.access_log.info(self.format_request())

    def access(self, resp, req, environ, request_time) -> None:
        """
        "gunicorn.access" logs are normally parsed here; however, the use
        of socketio and geventwebsocket worker overrides the "gunicorn.access"
        logger. Open issue: https://gitlab.com/noppo/gevent-websocket/-/issues/16

        :param resp:
        :param req:
        :param environ:
        :param request_time:
        :return:
        """
        ...
