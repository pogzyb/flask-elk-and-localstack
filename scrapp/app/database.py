from datetime import datetime
from typing import List

from flask_sqlalchemy import SQLAlchemy
from flask import current_app

from .search import search

db = SQLAlchemy()


class TimeMixin:
    """Generic Timestamp Mixin"""
    __table_args__ = {'extend_existing': True}

    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())


class CRUDMixin:
    """Generic Mixin for CRUD operations"""
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id: int):
        obj = cls.query.get(id).first_or_none()
        return obj

    @classmethod
    def get_by_ids(cls, ids: List[int]):
        objs = cls.query.filter(cls.id.in_(ids)).all()
        return objs

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


class SearchMixin(CRUDMixin):
    """SQLA Model Interface for Search"""
    @classmethod
    def from_search(cls, index_name: str, query_text: str, size: int):
        if not current_app.elasticsearch:
            return None
        else:
            obj_ids, num = search(index_name, query_text, size)
            objs = cls.get_by_ids(obj_ids)
            return objs
