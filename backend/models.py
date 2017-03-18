
"""SQLAlchemy database models. Imported by backend app."""

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, BigInteger, DateTime, Text, DECIMAL, VARCHAR
import datetime
import pymysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Photo(Base):
  __tablename__ = 'photo'
  id = Column(BigInteger, primary_key=True)
  uploadedTime = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
  caption = Column(Text(convert_unicode=True))
  language = Column(VARCHAR(10), nullable=False)
  views = Column(Integer, default=0, nullable=False)
  fileName = Column(Text(convert_unicode=True), nullable=False)
  lat = Column(DECIMAL(9,6), nullable=False)
  lon = Column(DECIMAL(9,6), nullable=False)
  upvotes = Column(Integer, default=0, nullable=False)
  downvotes = Column(Integer, default=0, nullable=False)

engine = create_engine('mysql+pymysql://root@localhost/swagswag')

Base.metadata.create_all(engine)
