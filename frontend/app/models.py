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


# TODO: does "user_loader" have to be here?
@login.user_loader
def load_user(id: str) -> int:
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'frontend_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(1000), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    # api_keys = relationship()

    def __repr__(self) -> str:
        return self.email

    def set_password_hash(self, password_input: str) -> None:
        self.password_hash = generate_password_hash(password_input)

    def check_password(self, password_input: str) -> bool:
        return check_password_hash(self.password_hash, password_input)

    def get_reset_password_token(self, expires: int = 600) -> str:
        salt = os.getenv('APP_SECRET_KEY')
        token = jwt.encode({'reset_password': self.id, 'expires': time() + expires}, salt, algorithm='HS256')
        logger.info(f"Token: {token.decode('utf-8')}")
        return token.decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token: str) -> Union['User', None]:
        try:
            salt = os.getenv('APP_SECRET_KEY')
            data = jwt.decode(token, salt, algorithms=['HS256'])
            user = User.query.get(data.get('reset_password'))
            return user
        except Exception as e:
            logger.exception(e)
            return


# class APIKey(db.Model):
#     __tablename__ = 'api_key'
#     id = db.Column(db.Integer, primary_key=True)
#     api_key = db.Column(db.String(256), unique=True, nullable=False)
#     num_calls = db.Column(db.Integer, default=0)
