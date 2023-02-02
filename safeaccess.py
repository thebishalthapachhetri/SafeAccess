

#!/usr/bin/env python3
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import http.client
import Adafruit_DHT
import os
import time

from smbus import SMBus
from mlx90614 import MLX90614

import urllib
import time
key = "43JXNDSG9BB20Z07"  # API KEY
temp = 0
rfid = 27.5
rfid_final = 123456

sensor = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)

def thermometer(rf_val):

#def thermometer():

    bus = SMBus(1)
    sensor = MLX90614(bus, address=0x5A)
    a_tempr = sensor.get_ambient()
    t_tempr = sensor.get_object_1()
    #print(rfid_final)
    #print("Ambient:", a_tempr)
    print("Target:", t_tempr+7)
    dhthum, dhttemp = Adafruit_DHT.read_retry(11,4)
    print ('Temperature of surroundings: {0:0.1f} C  Humidity: {1:0.1f} %'.format(dhttemp, dhthum))
   #os.system("face_mask_detection/detect.py")
    cmd = os.path.join(os.getcwd(), "detect.py")
    if dhttemp < 40:
        if t_tempr+7 > 37.5:
            print ("Access denied. you have a fever")
        else:
            os.system('{} {}'.format('python3', cmd))
    else:
       print ("Environment temperature is high")       
       os.system('{} {}'.format('python3', cmd))
       
    #print ("Ambient Temperature :", sensor.get_ambient())
    #print ("Object Temperature :", sensor.get_object_1())
    #temp = sensor.get_object_1()
    bus.close()
    #GPIO.cleanup()
        
    params = urllib.parse.urlencode({'field1': (float(rf_val)) , 'field2': t_tempr, 'key':key }) 
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print (temp)
            print (response.status, response.reason)
            data = response.read()
            conn.close()
    except:
            print  ("connection failed")
    
        

def readRFID():
    reader = SimpleMFRC522()
    try:
        print("Please scan your Card or Tag")
        rfid, rfidResponse = reader.read()
        print("Waiting for RFID")
        print(rfid)
        print("Place your hand in front of sensor")
        while True:
            if not GPIO.input(sensor):
                print("Hand detected")
                break
        
    finally:
       GPIO.cleanup()
    return rfid
    
while True:
        #readRFID()
        #thermometer()
    #GPIO.cleanup()    
	thermometer(readRFID())
    #GPIO.cleanup()
