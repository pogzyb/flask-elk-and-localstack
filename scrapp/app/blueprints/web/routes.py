
from structlog import get_logger
from flask_login import current_user, login_required
from flask import render_template

from . import web


logger = get_logger()


@web.route('/')
def index():
    return render_template('web/index.html')
