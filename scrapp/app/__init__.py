import os
from logging.config import dictConfig

from flask import Flask, render_template
from requests import codes
from elasticsearch import Elasticsearch
import structlog

from app.assets import assets
from app.database import db
from app.extensions import cache, login, mail, migrate, socketio, marshmallow
from app.blueprints import api, auth, term, web
from app.loggers import LoggerConfig
from config import get_app_config


dictConfig(LoggerConfig(name=__name__).dict_config)
structlog.configure(
    processors=[
        structlog.threadlocal.merge_threadlocal,
        # This performs the initial filtering, so we don't
        # evaluate e.g. DEBUG when unnecessary
        structlog.stdlib.filter_by_level,
        # Adds logger=module_name (e.g __main__)
        structlog.stdlib.add_logger_name,
        # Adds level=info, debug, etc.
        structlog.stdlib.add_log_level,
        # Performs the % string interpolation as expected
        structlog.stdlib.PositionalArgumentsFormatter(),
        # Include the stack when stack_info=True
        structlog.processors.StackInfoRenderer(),
        # Include the exception when exc_info=True
        # e.g log.exception() or log.warning(exc_info=True)'s behavior
        structlog.processors.format_exc_info,
        # Decodes the unicode values in any kv pairs
        structlog.processors.UnicodeDecoder(),
        # Creates the necessary args, kwargs for log()
        # structlog.stdlib.render_to_log_kwargs,  # <-- pain in the ass
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter
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
        env = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(get_app_config(env))
    app.logger = structlog.get_logger()

    with app.app_context():
        es_uri = app.config.get('ELASTICSEARCH_URL')
        if es_uri:
            # setup conn
            es = get_elasticsearch_client(es_uri)
            # create index
            index_name = os.getenv('ELASTICSEARCH_INDEX_NAME')
            es.indices.create(index=index_name, ignore=400)
            # store elasticsearch client into global namespace
            app.elasticsearch = es

        register_extensions(app)
        register_blueprints(app)
        register_errorhandlers(app)
        register_jinja_env(app)

    return app


def get_elasticsearch_client(uri: str):
    es = Elasticsearch(
        [uri],
        sniff_on_start=True,
        sniff_on_connection_fail=True,
        sniffer_timeout=60)
    return es


def register_extensions(app: Flask):
    """Register Flask-Plugin modules"""
    assets.init_app(app)
    db.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    marshmallow.init_app(app)
    login.init_app(app)
    login.blueprint_login_views = {'auth': '/login'}
    from app.blueprints.term import events  # necessary for socketio
    socketio.init_app(app, async_mode=None)


def register_blueprints(app: Flask):
    """Register the Blueprints"""
    app.register_blueprint(term)
    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(web)


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
