import os, sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
import subprocess
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import bluepy
import micropyGPS
import serial
import time
import json
from myconfig import configmaker
from db import models

# read a config file
configIni = configmaker.read_config()

# create a database engine
db = configIni['DB']
dbPath = db.get('path')
engine = sqlalchemy.create_engine('sqlite:///' + dbPath, echo=False)
models.Base.metadata.create_all(bind=engine)

# BD Address
bdAddress = configIni['BDAddress']
# RASPBERRY_BD_ADDRESS = bdAddress.get('raspberryPi')
DONGLE_BD_ADDRESS = bdAddress.get('dongle')

# select BLE device
hciconfig = subprocess.run(["hciconfig"], capture_output=True, text=True).stdout
# [TODO] when this raspberry pi doesn't detect the USB dongle, write an error message.
if hciconfig.count(DONGLE_BD_ADDRESS) == 0:
    print("[Warning] You may not be using a usb dongle. Please check BD Address of config.ini")
    sys.exit()

hciTxt = hciconfig.split(DONGLE_BD_ADDRESS)[0]
hciIndex = hciTxt.rfind("hci") + 3
scanner = bluepy.btle.Scanner(str(hciTxt[hciIndex]))

gps = micropyGPS.MicropyGPS(9, 'dd')

print("---Save Data---")
print("| scan_time | latitude | longitude | addr_num |")

### START SCAN ###
while True:
    try:
        s = serial.Serial('/dev/serial0', 9600, timeout=1000)
        s.readline()
        sentence = s.readline().decode('utf-8')
        if sentence[0] != '$': # 先頭が$でなければ捨てる
            continue
        for x in sentence:
            gps.update(x)
    except:
        pass
        
    latitude = gps.latitude[0]
    longitude = gps.longitude[0]
    scanTime = int(time.time())
    
    bleList = []
    try:
        devices = scanner.scan(10)
        for device in devices:
            ble = {}
            ble["addr"] = device.addr
            ble["rssi"] = device.rssi
            bleList.append(ble)
    except:
        pass
        
    bleJson = json.dumps(bleList) # convert python object to str(json obj)
    
    # save to a database
    session = sessionmaker(bind=engine)()
    sensor = models.Sensor()
    sensor.t = scanTime
    sensor.lat = latitude
    sensor.lng = longitude
    sensor.ble = bleJson
    
    session.add(instance=sensor)
    session.commit()
    
    
    print("| {} | {} | {} | {} |".format(scanTime, latitude, longitude, len(bleList)))
    # print(bleJson)
    
    time.sleep(5)
