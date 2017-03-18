"""SQLAlchemy database models. Imported by backend app."""

import datetime

import pymysql
from __init__ import db


class Photo(db.Model):
    """Photo table."""

    id = db.Column(db.BigInteger, primary_key=True)
    uploadedTime = db.Column(db.DateTime,
                             default=datetime.datetime.utcnow, nullable=False)
    caption = db.Column(db.Text(convert_unicode=True))
    language = db.Column(db.VARCHAR(10), nullable=False)
    views = db.Column(db.Integer, default=0, nullable=False)
    fileName = db.Column(db.Text(convert_unicode=True), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    likes = db.Column(db.Integer, default=0, nullable=False)
    dislikes = db.Column(db.Integer, default=0, nullable=False)

    viewedby = db.relationship(
        'User',
        secondary='user_viewed_photo'
    )


class User(db.Model):
    """User table, handles auth."""

    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.VARCHAR(20), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    viewed = db.relationship(
        'Photo',
        secondary='user_viewed_photo',
    )


class UserViewedPhoto(db.Model):
    """Middleman table for M2M relationships for viewed photos."""

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    photo_id = db.Column(db.BigInteger, db.ForeignKey(
        'photo.id'), primary_key=True)
