from flask_caching import Cache
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_marshmallow import Marshmallow

from app.email import MailExecutor

cache = Cache()
mail = MailExecutor()
login = LoginManager()
socketio = SocketIO()
migrate = Migrate()
marshmallow = Marshmallow()
