import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
import time
import datetime
from datetime import timedelta
from orm import Session
from orm.models import Sensor

while True:
    # get time
    dtNow = datetime.datetime.now() # now
    timeDelta = timedelta(days=7) # 7 days
    daysAgo = int((dtNow-timeDelta).timestamp()) # 7 days ago (UNIX timestamp integer)

    # delete records
    session = Session()
    session.query(Sensor).filter(Sensor.t <= daysAgo).delete()
    session.commit()
    session.close()

    time.sleep(86400)
