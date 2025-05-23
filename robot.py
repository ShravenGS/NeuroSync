from gpiozero import LED
import RPi.GPIO as GPIO
from gpiozero import Button,MCP3008
from time import sleep
import requests
import time
from heartrate_monitor import HeartRateMonitor,hb,spo2m
import time
import argparse
import os
import glob
import time
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c


parser = argparse.ArgumentParser(description="Read and print data from MAX30102")
parser.add_argument("-r", "--raw", action="store_true",
                    help="print raw data instead of calculation result")
parser.add_argument("-t", "--time", type=int, default=30,
                    help="duration in seconds to read from sensor, default 30")
args = parser.parse_args()


print('sensor starting...')
hrm = HeartRateMonitor(print_raw=args.raw, print_result=(not args.raw))
hrm.start_sensor()


m1=LED(21)
m2=LED(20)
m3=LED(16)
m4=LED(12)

m1.off()
m2.off()
m3.off()
m4.off()

hbt=0
lt=0


while True:    
        r =requests.get('http://iotclouddata.com/24log/377/getstatus1.php')
        print('Resp:'+r.text)
        print('Temperature:'+str(read_temp()))
        if r.text[0]=='0' and lt !=1:
                m1.off()
                m2.off()
                m3.off()
                m4.off()                
                lt=1
        elif r.text[0]=='1' and lt !=2:
                m1.off()
                m2.on()
                m3.off()
                m4.on()                
                lt=2                
        elif r.text[0]=='2' and lt !=3:
                m1.on()
                m2.off()
                m3.on()
                m4.off()                
                lt=3
        elif r.text[0]=='3' and lt !=4:
                m1.on()
                m2.off()
                m3.on()
                m4.off()
                lt=4
        elif r.text[0]=='5' and lt !=5:
                m1.off()
                m2.off()
                m3.off()
                m4.off()                
                lt=5                
        else:
                m1.off()
                m2.off()
                
                m3.off()
                m4.off()                
        sleep(2)
        m1.off()
        m2.off()
        m3.off()
        m4.off()                
        
        
        