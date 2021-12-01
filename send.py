import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
import time
from sqlalchemy import inspect
import urllib.request
import json
from myconfig import configmaker
from orm import Session
from orm.models import Sensor

# read a config file
configIni = configmaker.read_config()

# setting
api = configIni['API']
url = api.get('url')
key = api.get('key')
method = api.get('method')

meta = configIni['Meta']
area = meta.getint('area')
type_ = meta.getint('type')
sensorID = meta.get('sensorID')

bleColName = 'ble'

# toDict: convert a sqlalchemy object to a dict(python object)
def toDict(record):
    return {c.key: getattr(record, c.key) for c in inspect(record).mapper.column_attrs}
    
# bleToList: convert type of ble column from str to list
def bleToList(record, colName):
    record[colName] = json.loads(record[colName])
    return record

while True:
    # send data
    session = Session()
    records = session.query(Sensor).filter((Sensor.flag == 0) & (Sensor.ble != '[]')).all() # select data for post
    if records:
        dictRecords = [toDict(record) for record in records] # convert type of record
        newDictRecords = [bleToList(record, bleColName) for record in dictRecords] # convert type of ble column of record
        data_time = newDictRecords[0]['t']
        
        # delete not post columns
        for dictRecord in newDictRecords:
            del dictRecord['id'], dictRecord['created_at'], dictRecord['flag']
            
        postDataDict = {
            "key": key,
            "meta": {
                "area": area,
                "type": type_,
                "sensor_id": sensorID,
                "data_time": data_time,
            },
            "body": newDictRecords
        }

        postData = json.dumps(postDataDict) # convert dict record to json record for post
        # print(postData)
        
        # POST
        request = urllib.request.Request(
            url = url,
            data = postData.encode('utf-8'),
            method = method
        )

        try:
            with urllib.request.urlopen(request) as response:
                body = response.read()
            print(response.getcode())

            # update flag of sent data
            print("[Transmission completed!]")
            print("| id | scan_time | latitude | longitude | addr_num |")
            for record in records:
                print("| {} | {} | {} | {} | {} |".format(record.id, record.t, record.lat, record.lng, int(len(record.ble)/44)))
                record.flag = 1
            session.commit()
            print("------------------------------")
        except urllib.error.HTTPError as err:
            print(err.code)
            pass
        except urllib.error.URLError as err:
            print(err.reason)
            pass
    
    else:
        print("[All data has been sent...]")
        pass

    session.close()
    
    time.sleep(20)