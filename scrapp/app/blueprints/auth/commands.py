
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError

from . import auth
from .models import User, Role


@auth.cli.command("create-admin")
@with_appcontext
def create_admin():
    try:
        User.create(
            email='admin@email.com',
            password='admin123',
            roles=[Role.create(name='admin')],
            active=True)
    except IntegrityError:
        ...
