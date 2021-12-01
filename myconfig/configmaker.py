import os
import configparser
import errno

def read_config():
    configIni = configparser.ConfigParser()
    configIniPath = 'myconfig/config.ini'
    if not os.path.exists(configIniPath):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), configIniPath)
    configIni.read(configIniPath, encoding='utf-8')
    
    return configIni
