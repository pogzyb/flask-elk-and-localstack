from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = 'frontend_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=False, unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.email