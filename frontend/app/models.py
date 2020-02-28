from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


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
    # api_keys =

    def __repr__(self) -> str:
        return self.email

    def set_password_hash(self, password_input: str) -> None:
        self.password_hash = generate_password_hash(password_input)

    def check_password(self, password_input: str) -> bool:
        return check_password_hash(self.password_hash, password_input)


# class APIKey(db.Model):
#     __tablename__ = 'api_key'
#     id = db.Column(db.Integer, primary_key=True)
#     api_key = db.Column(db.String(256), unique=True, nullable=False)
#     num_calls = db.Column(db.Integer, default=0)
