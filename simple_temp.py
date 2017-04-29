import os
import glob
import time
import RPi.GPIO as GPIO

os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')
device_files = [folder + '/w1_slave' for folder in device_folders]

green_led_temp = 22.0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)

def set_green_led(val):
    GPIO.output(18, GPIO.HIGH if val else GPIO.LOW)

def get_temps():
    temps = []
    for device_file in device_files:
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        if lines[0].find('YES') != -1:
            pos = lines[1].find('t=')
            if pos != -1:
                temps.append(float(lines[1][pos+2:]) / 1000.0)
    return temps

while True:
    temps = get_temps()
    if len(temps) > 0:
        print(temps)
        set_green_led(temps[0] > green_led_temp)
    time.sleep(1)

