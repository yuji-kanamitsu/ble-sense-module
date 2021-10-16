import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, Float, Integer, String, DateTime
import datetime
import json

Base = declarative_base()

class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    flag = Column(Integer, default=0) # flag == 0 -> means not sent yet
    scan_time = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    ble = Column(String)
