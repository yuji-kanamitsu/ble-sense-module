import os, sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
import configparser
import errno
import time
import datetime
from datetime import timedelta
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from db import models
from db.models import Sensor

# Change a current directly
os.chdir('/home/pi/Documents/ble-sense-module')

# Read a config file
configIni = configparser.ConfigParser()
configIniPath = 'config.ini'
if not os.path.exists(configIniPath):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), configIniPath)
configIni.read(configIniPath, encoding='utf-8')

# Setting DB
db = configIni['DB']
dbName = db.get('name')
engine = sqlalchemy.create_engine('sqlite:///db/' + dbName + '.sqlite3', echo=False)
models.Base.metadata.create_all(bind=engine)

while True:
    # now
    dtNow = datetime.datetime.now()
    print(dtNow)

    # 7 days
    timeDelta = timedelta(days=7)
    print(timeDelta)

    # 7 days ago (UNIX timestamp integer)
    daysAgo = int((dtNow-timeDelta).timestamp())

    # select records
    session = sessionmaker(bind=engine)()
    records = session.query(Sensor).filter(Sensor.t <= daysAgo).all()
    print(records)

    # if (scan_time < now - 7days) -> delete
    print(dtNow - timeDelta)

    # time.sleep(86400)