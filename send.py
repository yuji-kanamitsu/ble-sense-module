import os
import time
import sqlalchemy
# from sqlalchemy import and_, or_, not_
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
import urllib.request
import configparser
import json
from db.models import Sensor

# Read a config file
configIni = configparser.ConfigParser()
configIniPath = 'config.ini'
if not os.path.exists(configIniPath):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), configIniPath)
configIni.read(configIniPath, encoding='utf-8')

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
    # create database engine
    # engine = sqlalchemy.create_engine('sqlite:///db/test_db.sqlite3', echo=True)
    engine = sqlalchemy.create_engine('sqlite:///db/test_db.sqlite3', echo=False)
    session = sessionmaker(bind=engine)()

    # send data
    records = session.query(Sensor).filter((Sensor.flag == 0) & (Sensor.ble != '[]')).all() # select data for post
    if records:
        # selectedIdList = [record.id for record in records] # use update phase later
        # print(selectedIdList)
        
        dictRecords = [toDict(record) for record in records] # convert type of record
        newDictRecords = [bleToList(record, bleColName) for record in dictRecords] # convert type of ble column of record
        data_time = newDictRecords[0]['scan_time']
        # print("'data_time: {}' is the scan_time of the first record (id: {})".format(data_time, newDictRecords[0]['id']))
        
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
        #request = urllib.request.Request(
        #    url = url,
        #    data = postData,
        #    method = method
        #)

        #try:
        #    with urllib.request.urlopen(request) as response:
        #        body = response.read()
        #except urllib.error.HTTPError as err:
        #    print(err.code)
        #    pass
        #except urllib.error.URLError as err:
        #    print(err.reason)
        #    pass
        
        '''
        set a flag
        '''
        # update flag of sent data
        print("[Transmission completed!]")
        print("---Sent Data---")
        print("| id | scan_time | latitude | longitude | addr_num |")
        for record in records:
            print("| {} | {} | {} | {} | {} |".format(record.id, record.scan_time, record.latitude, record.longitude, int(len(record.ble)/44)))
            record.flag = 1
        session.commit()
        print("------------------------------")
    
    else:
        print("[All data has been sent...]")
        pass
    
    time.sleep(20)
