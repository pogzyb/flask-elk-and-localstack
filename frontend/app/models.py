import logging
import os
from typing import Union
from time import time
from datetime import datetime

import jwt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


logger = logging.getLogger(__name__)


@login.user_loader
def load_user(id: str) -> int:
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(1000), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    # roles =

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
        return token.decode('utf-8')

    @staticmethod
    def verify_token(token: str, key: str) -> Union['User', None]:
        try:
            salt = os.getenv('APP_SECRET_KEY')
            data = jwt.decode(token, salt, algorithms=['HS256'])
            user = User.query.get(data.get(key))
            return user
        except:
            logger.exception(f'Could not reset password:')
