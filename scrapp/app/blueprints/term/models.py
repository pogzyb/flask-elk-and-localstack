from enum import Enum

from sqlalchemy import Table, Column, Integer, ForeignKey

from app.database import db, SearchMixin, TimeMixin


class ScrapeStatus(str, Enum):
    PENDING = 'pending'
    COMPLETE = 'complete'
    TIMEOUT = 'timeout'


assoc_item_link = Table(
    'assoc_term_link',
    db.metadata,
    Column('term_id', Integer, ForeignKey('term.id')),
    Column('link_id', Integer, ForeignKey('link.id')))


class Term(SearchMixin, TimeMixin, db.Model):
    __tablename__ = 'term'
    __searchable__ = ['term']
    term = db.Column(db.String(250), nullable=False)
    # standing = db.Column(db.Enum(), default=ScrapeStatus.PENDING)
    links = db.relationship('Link',
                            secondary=assoc_item_link,
                            back_populates='terms')


class Link(SearchMixin, TimeMixin, db.Model):
    __tablename__ = 'link'
    __searchable__ = ['href', 'domain']
    subdomain = db.Column(db.String(250))
    domain = db.Column(db.String(250), nullable=False)
    tld = db.Column(db.String(250), nullable=False)
    href = db.Column(db.String(250), nullable=False)
    terms = db.relationship('Term',
                            secondary=assoc_item_link,
                            back_populates='links')
