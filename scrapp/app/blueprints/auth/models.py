import os
import collections
from typing import Union
from time import time
from datetime import datetime

import jwt
from structlog import get_logger
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

from app import login
from app.database import db, CRUDMixin

logger = get_logger(__name__)


@login.user_loader
def load_user(_id: str) -> int:
    return User.query.get(int(_id))


class Role(db.Model):
    """
    Role table: stores information about roles, which users can be tied to users
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    """
    Association table for Users and Roles
    """
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class User(CRUDMixin, UserMixin, db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(1000), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=False)
    roles: collections.Iterable = relationship('Role', secondary='user_roles')

    def __repr__(self) -> str:
        return self.email

    def __str__(self):
        return self.email

    @property
    def password(self):
        raise AttributeError('password_hash is not a readable attribute')

    @password.setter
    def password(self, password_input: str) -> None:
        self.password_hash = generate_password_hash(password_input)

    def check_password(self, password_input: str) -> bool:
        return check_password_hash(self.password_hash, password_input)

    def generate_token(self, key: str, expires: int = 600) -> str:
        salt = os.getenv('APP_SECRET_KEY')
        token = jwt.encode({key: self.id, 'expires': time() + expires}, salt, algorithm='HS256')
        return token

    @staticmethod
    def verify_token(token: str, key: str) -> Union['User', None]:
        try:
            salt = os.getenv('APP_SECRET_KEY')
            data = jwt.decode(token, salt, algorithms=['HS256'])
            user = User.get_by_id(data.get(key))
            return user
        except:
            logger.exception(f'could not reset password:')
            return None
