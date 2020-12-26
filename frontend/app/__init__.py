import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_caching import Cache

from config import get_config
from app.email import MailExecutor

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger(__name__).setLevel(logging.DEBUG)

db = SQLAlchemy()
login = LoginManager()
socketio = SocketIO()
cache = Cache()
mail = MailExecutor()


def create_app(env: str = None):
    """
    Factory function sits atop the application
    :return: Flask application
    """
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(get_config(env))

    # init plugins
    db.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    login.init_app(app)
    login.blueprint_login_views = {'auth': '/login'}
    from app.blueprints.web import events  # necessary for socketio
    socketio.init_app(app, async_mode=None)

    with app.app_context():
        from app.blueprints import api, auth, web
        app.register_blueprint(web)
        app.register_blueprint(api)
        app.register_blueprint(auth)

        db.create_all()

    return app
