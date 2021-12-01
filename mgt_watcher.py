import subprocess, os
import datetime
import time

sensor_name = "blescanner"

proc_title = "iopt_" + sensor_name

# d = datetime.datetime.now()

check_result = subprocess.getoutput('ps -ef | grep "' + proc_title + '" | grep -v grep') != ""
print("Is IoPT sensor is running? : ", check_result)

if (not check_result):
	print("restart IoPT sensor")
	os.system("sudo python3 sense.py & python3 send.py & python3 delete.py &")
	
	time.sleep(60)
	
	print("send email")
	# create_and_send_message()