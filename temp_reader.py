import os
import serial
import glob
import sys
from time import sleep
from datetime import datetime

bluetooth_sensors = [(0, '00:14:03:06:0B:DD', 1, 9600, 'outside temp cold')]
#bluetooth_sensors = [(1, '4C:74:03:63:C0:76', 2, 19200, 'outside temp warm')]
REQUEST_TEMPERATURE = "REQ_TEMP"
RESPONSE_TEMPERATURE = "RES_TEMP"
LOCAL_SENSORS_BASE_PATH = '/sys/bus/w1/devices/'

class BluetoothSensor:

    def __init__(self, name, device_number, baudrate):
        self.port = serial.Serial("/dev/rfcomm" + str(device_number),
                                  baudrate=baudrate)
        self.name = name
        sleep(5)

    def get_temp(self):
        try:
            #print ("request", self.name)
            self.port.write(REQUEST_TEMPERATURE.encode('ascii'))
            sleep(2)
            ret = self.port.read(self.port.inWaiting()).decode('ascii')
            #print("response", self.name, ret)
            if ret.startswith(RESPONSE_TEMPERATURE):
                return float(ret[len(RESPONSE_TEMPERATURE):])
            return None
        except:
            #print(str(sys.exc_info()[0]))
            return None

            
class LocalSensor:

    def __init__(self, name, path):
        self.path = path
        self.name = name

    def get_temp(self):
        try:
            f = open(self.path, 'r')
            lines = f.readlines()
            f.close()
            if lines[0].find('YES') != -1:
                pos = lines[1].find('t=')
                if pos != -1:
                    return float(lines[1][pos+2:]) / 1000.0
            return None
        except:
            return None
        

def init():
    print ("Initializing bluetooth devices...")
    for b in bluetooth_sensors:
        print ("Initializing device", b[0], "MAC", b[1], "channel", b[2])
        os.system("sudo rfcomm bind {} {} {}".format(b[0], b[1], b[2]))
    print ("Initializing local devices...")
    os.system('sudo modprobe w1-gpio')
    os.system('sudo modprobe w1-therm')


def get_all_temperature_sensors():
    sensors = [BluetoothSensor(b[4], b[0], int(b[3]))
               for b in bluetooth_sensors]
    paths = [folder + '/w1_slave'
             for folder in glob.glob(LOCAL_SENSORS_BASE_PATH + '28*')]
    sensors += [LocalSensor("inside temp #" + str(i+1), path)
                for (i, path) in zip(range(len(paths)), paths)]
    return sensors


if __name__ == '__main__':
    init()
    sensors = get_all_temperature_sensors()
    while True:
        with open('temps.csv', 'a') as f:
            for sensor in sensors:
                temp = sensor.get_temp()
                if temp is not None:
                    print(sensor.name, temp)
                    f.write("{},{},{}\n".format(datetime.now(), sensor.name, temp))
        sleep(1)
