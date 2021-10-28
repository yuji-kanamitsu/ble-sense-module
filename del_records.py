import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
import time
import datetime
from datetime import timedelta
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from myconfig import configmaker
from db import models
from db.models import Sensor

# Read a config file
configIni = configmaker.read_config()

# Setting DB
db = configIni['DB']
dbPath = db.get('path')
engine = sqlalchemy.create_engine('sqlite:///' + dbPath, echo=False)
models.Base.metadata.create_all(bind=engine)

while True:
    # get time
    dtNow = datetime.datetime.now() # now
    timeDelta = timedelta(days=7) # 7 days
    daysAgo = int((dtNow-timeDelta).timestamp()) # 7 days ago (UNIX timestamp integer)

    # delete records
    session = sessionmaker(bind=engine)()
    session.query(Sensor).filter(Sensor.t <= daysAgo).delete()
    session.commit()

    time.sleep(86400)
