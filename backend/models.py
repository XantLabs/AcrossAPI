"""SQLAlchemy database models. Imported by backend app."""

import datetime

import pymysql

from . import db

Base = declarative_base()


class Photo(Base):
    """Photo table."""

    id = db.Column(db.BigInteger, primary_key=True)
    uploadedTime = db.Column(DateTime,
                             default=datetime.datetime.utcnow, nullable=False)
    caption = db.Column(Text(convert_unicode=True))
    language = db.Column(VARCHAR(10), nullable=False)
    views = db.Column(Integer, default=0, nullable=False)
    fileName = db.Column(Text(convert_unicode=True), nullable=False)
    lat = db.Column(DECIMAL(9, 6), nullable=False)
    lon = db.Column(DECIMAL(9, 6), nullable=False)
    likes = db.Column(Integer, default=0, nullable=False)
    dislikes = db.Column(Integer, default=0, nullable=False)
    viewedby = relationship(
        'User',
        secondary='user_viewed_photo'
    )


class User(Base):
    """User table, handles auth."""

    id = db.Column(Integer, primary_key=True)
    language = db.Column(VARCHAR(10), nullable=False)
    viewed = relationship(
        'Photo',
        secondary='user_viewed_photo',
    )


class UserViewedPhoto(Base):
    """Middleman table for M2M relationships for viewed photos."""

    user_id = db.Column(Integer, db.ForeignKey('user.id'), primary_key=True)
    photo_id = db.Column(db.BigInteger, db.ForeignKey(
        'photo.id'), primary_key=True)
