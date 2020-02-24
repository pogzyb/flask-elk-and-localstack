from flask import Blueprint

web = Blueprint('web', __name__, template_folder='templates/web')

from app.blueprints.web import handlers
