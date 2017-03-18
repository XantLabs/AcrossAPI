"""SQLAlchemy database models. Imported by backend app."""

import datetime

import pymysql
from sqlalchemy import (DECIMAL, VARCHAR, BigInteger, Column, DateTime,
                        ForeignKey, Integer, MetaData, String, Table, Text,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

Base = declarative_base()


class Photo(Base):
    """Photo table."""

    __tablename__ = 'photo'

    id = Column(BigInteger, primary_key=True)
    uploadedTime = Column(DateTime,
                          default=datetime.datetime.utcnow, nullable=False)
    caption = Column(Text(convert_unicode=True))
    language = Column(VARCHAR(10), nullable=False)
    views = Column(Integer, default=0, nullable=False)
    fileName = Column(Text(convert_unicode=True), nullable=False)
    lat = Column(DECIMAL(9, 6), nullable=False)
    lon = Column(DECIMAL(9, 6), nullable=False)
    likes = Column(Integer, default=0, nullable=False)
    dislikes = Column(Integer, default=0, nullable=False)
    viewedby = relationship(
        'User',
        secondary='user_viewed_photo'
    )


class User(Base):
    """User table, handles auth."""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    language = Column(VARCHAR(10), nullable=False)
    viewed = relationship(
        'Photo',
        secondary='user_viewed_photo',
    )


class UserViewedPhoto(Base):
    """Middleman table for M2M relationships for viewed photos."""

    __tablename__ = 'user_viewed_photo'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    photo_id = Column(BigInteger, ForeignKey('photo.id'), primary_key=True)


engine = create_engine('mysql+pymysql://root@localhost/swagswag')
Base.metadata.create_all(engine)
