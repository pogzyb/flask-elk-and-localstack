import os
from logging.config import dictConfig

from flask import Flask, render_template
from requests import codes
import structlog

from app.database import db
from app.extensions import cache, login, mail, migrate, socketio
from app.blueprints import api, auth, web
from app.loggers import LoggerConfig
from config import get_app_config


dictConfig(LoggerConfig(name=__name__).dict_config)
structlog.configure(
    processors=[
        structlog.threadlocal.merge_threadlocal,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.render_to_log_kwargs,
        # structlog.processors.JSONRenderer()
        # ^-- don't need it; handled by the json formatter in LoggerConfig().dict_config
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True)


def create_app(env: str = None):
    """
    Factory function sits atop the application
    :return: Flask application
    """
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(get_app_config(env))
    app.logger = structlog.get_logger()

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_jinja_env(app)

    return app


def register_extensions(app: Flask):
    """Register Flask-Plugin modules"""
    db.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.blueprint_login_views = {'auth': '/login'}
    from app.blueprints.web import events  # another necessity for socketio
    socketio.init_app(app, async_mode=None)


def register_blueprints(app: Flask):
    """Register the Blueprints"""
    app.register_blueprint(web)
    app.register_blueprint(api)
    app.register_blueprint(auth)


def register_errorhandlers(app: Flask):
    """Register Error Handlers for 404 and 500 statuses"""

    def render_error(err):
        return render_template('errors/%s.html' % err.code), err.code

    for e in [codes.INTERNAL_SERVER_ERROR, codes.NOT_FOUND]:
        app.errorhandler(e)(render_error)


def register_jinja_env(app: Flask):
    """Adds global functions into Jinja env"""
    app.jinja_env.globals.update({
        'app_version': os.getenv('APP_VERSION', 'debug')})
