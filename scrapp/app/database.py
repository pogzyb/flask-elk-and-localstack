from structlog import get_logger
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
logger = get_logger(__name__)


class CRUDMixin:
    """Generic Mixin for CRUD operations"""
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id: int):
        obj = cls.query.get(id).first_or_none()
        return obj

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        return obj.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            if getattr(self, attr):
                setattr(self, attr, value)

        if commit:
            return self.save()
        else:
            return self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()


class DataTable:
    pass
