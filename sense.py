import os, sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
import configparser
import subprocess
import errno
# import sqlite3
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import bluepy
import micropyGPS
import serial
import datetime
from models.sensor import Sensor

# Read a config file
configIni = configparser.ConfigParser()
configIniPath = 'config.ini'
if not os.path.exists(configIniPath):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), configIniPath)
configIni.read(configIniPath, encoding='utf-8')

# Connect a database
engine = sqlalchemy.create_engine('sqlite:///test_db.sqlite3', echo=True)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


# BD Address
bdAddress = configIni['BDAddress']
RASPBERRY_BD_ADDRESS = bdAddress.get('raspberryPi')
DONGLE_BD_ADDRESS = bdAddress.get('dongle')

# Select BLE device
hciconfig = subprocess.run(["hciconfig"], capture_output=True, text=True).stdout
# [TODO] when this raspberry pi doesn't detect the USB dongle, write an error message.
if hciconfig.count(DONGLE_BD_ADDRESS) == 0:
    print("[Warning] You may not be using a usb dongle. Please check BD Address of config.ini")
    sys.exit()

hciTxt = hciconfig.split(DONGLE_BD_ADDRESS)[0]
hciIndex = hciTxt.rfind("hci") + 3
scanner = bluepy.btle.Scanner(str(hciTxt[hciIndex]))

gps = micropyGPS.MicropyGPS(9, 'dd')

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

    scanTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    bleList = []
    devices = scanner.scan(10)
    for device in devices:
        ble = {}
        ble["addr"] = device.addr
        ble["rssi"] = device.rssi
        bleList.append(ble)

    """
    save to database
    """
    session = sessionmaker(bind=engine)()
    sensingData = Sensor()
    sensingData.scan_time = scanTime
    sensingData.latitude = latitude
    sensingData.longitude = longitude
    sensingData.ble = bleList

    session.add(instance=sensingData)
    session.commit()