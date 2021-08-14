from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates/auth')

# imports below to avoid circular dependencies
from . import commands # noqa
from . import handlers # noqa
