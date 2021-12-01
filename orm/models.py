import datetime
from sqlalchemy import Column, Float, Integer, String, DateTime
from orm.base import Base

class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    flag = Column(Integer, default=0) # flag == 0 -> means not sent yet
    t = Column('scan_time', Integer)
    lat = Column('latitude', Float)
    lng = Column('longitude', Float)
    ble = Column('ble', String)
