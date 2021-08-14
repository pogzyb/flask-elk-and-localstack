from flask import Blueprint

term = Blueprint('term', __name__, url_prefix='/term', template_folder='templates/term')

from . import events, routes # noqa
