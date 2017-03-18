"""SQLAlchemy database models. Imported by backend app."""

import pymysql
from __init__ import app, db
from social_flask_sqlalchemy.models import init_social


class Photo(db.Model):
    """Photo table."""

    id = db.Column(db.BigInteger, primary_key=True)

    uploadedTime = db.Column(db.DateTime, nullable=False)

    caption = db.Column(db.Text(convert_unicode=True))
    language = db.Column(db.VARCHAR(10), nullable=False)

    views = db.Column(db.Integer, default=0, nullable=False)

    active = db.Column(db.Boolean, default=True, nullable=False)

    fileName = db.Column(db.Text(convert_unicode=True), nullable=False)

    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    likes = db.Column(db.Integer, default=0, nullable=False)
    dislikes = db.Column(db.Integer, default=0, nullable=False)


db.create_all()
db.session.commit()
