import sqlalchemy
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
import datetime
from sense import Base

class Sensor(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    flag = Column(Integer)
    scan_time = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    ble = Column(String)

    __tablename__ = 'sensors'




    