import os, sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
import errno
import bluepy
import micropyGPS
import serial
import datetime
import configparser
import subprocess

# Read a config file
configIni = configparser.ConfigParser()
configIniPath = 'config.ini'
if not os.path.exists(configIniPath):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), configIniPath)
configIni.read(configIniPath, encoding='utf-8')

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
    print(gps.latitude[0])
    print(gps.longitude[0])

    '''
    Write down the code of scanning ble data
    '''
    scanTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    print(scanTime)

    devices = scanner.scan(10)
    for device in devices:
        deviceAddr = device.addr
        deviceRssi = device.rssi
        print(deviceAddr)
        print(deviceRssi)
        """
        make json data
        """
        # bleData = {
        #     'addr': "hoge",
        #     'rssi': -43,
        # }

