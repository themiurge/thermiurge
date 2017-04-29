import serial
from time import sleep

# to start bletooth comm automatically:
# hcitool scan -> list of devices
# edit /etc/bluetooth/rfcomm.conf, add entries for all devices
# for each device, run
#     sudo rfcomm bind <dev no.> <MAC address> <channel>
# device is now /dev/rfcomm<dev no.>

REQUEST_TEMPERATURE = "REQ_TEMP"
RESPONSE_TEMPERATURE = "RES_TEMP"

s = serial.Serial("/dev/rfcomm0", baudrate=9600)
sleep(5)

while True:
    s.write(REQUEST_TEMPERATURE.encode('ascii'))
    sleep(2)
    ret = s.read(s.inWaiting())
    print(ret)
