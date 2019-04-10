################################################################################
# Energy Berry Main Loop 
#C
# Author Energy Berry Team
###############################################################################
import streams
import json
import requests
import rtc
import flash

from wireless import wifi
from servo import servo
from wireless import ble
from espressif.esp32ble import esp32ble as bledrv
from espressif.esp32net import esp32wifi as wifi_driver

pinMode(2,OUTPUT)
streams.serial()

def GetCurrentTime():
    wifi_driver.auto_init()
    # use the wifi interface to link to the Access Point
    # change network name, security and password as needed
    print("Establishing Link...")
    try:
        # FOR THIS EXAMPLE TO WORK, "Network-Name" AND "Wifi-Password" MUST BE SET
        # TO MATCH YOUR ACTUAL NETWORK CONFIGURATION
        wifi.link("Tuneros3000",wifi.WIFI_WPA2,"qwerty123")
    except Exception as e:
        print("ooops, something wrong while linking :(", e)
        return -1
    
    ## let's try to connect to timeapi.org to get the current UTC time
    for i in range(3):
        try:
            print("Trying to connect...")
            response = requests.get("http://worldtimeapi.org/api/timezone/America/Mexico_City")
            print("Http Status:",response.status)
            break
        except Exception as e:
            print(e)
    try:
        print("Success!!")
        print("-------------")
        print("And the result is:",response.content)
        print("-------------")
        js = json.loads(response.content)
        print("Time:",js["unixtime"])
        return js  
    except Exception as e:
        print("ooops, something very wrong! :(",e)
        return -1

timestamp = -1
while(timestamp == -1):
    print("Trying to get timestamp")
    jsTimeRes = GetCurrentTime()
    timestamp = int(jsTimeRes["unixtime"])

#    hardTimestamp = timestamp + 40
rtc.set_utc(timestamp)

#print("Trying to instert hardData in a flash file")
#flashFile = flash.FlashFileStream(0x00310000,512)
# [(DaySchedule) = int32]  [(timestamp) = int32]  [(NumPin = int16, DimmerLvl = int16) = int32]
#print("writing flash file")
#jsonFile = {
    #Estructura de Packetes 
#    "daySchedule":1111100,
#    "timestamp":hardTimestamp,
#    "numPin":2,
#    "dimmerLvl":100
#}
#jsonDs = json.dumps(jsonFile)
#save length and json to flash
#flashFile.write(len(ds))
#flashFile.write(jsonDs)
#flashFile.flush()

#BLE BLOCK INIT
bledrv.init()
# Set GAP name
ble.gap("Berry dimmer")
# Create a GATT Service: let's try a Battery Service (uuid is 0x180F)
s = ble.Service(0x180F)
sTime = ble.Service(0x1805)
# Create a GATT Characteristic
c = ble.Characteristic(0x2A58,ble.NOTIFY | ble.READ | ble.WRITE,1,"Battery Level",ble.NUMBER)
cTime = ble.Characteristic(0x2A2B,ble.NOTIFY | ble.READ | ble.WRITE,20,"Current Time",ble.STRING)
# Add the GATT Characteristic to the Service
s.add_characteristic(c)
sTime.add_characteristic(cTime)
ble.add_service(s)
ble.add_service(sTime)
# Start the BLE stack
ble.start()
ble.start_advertising()
c.set_value(0)

MyServo=servo.Servo(D5.PWM)
MyServo.attach()

while True:
    print(".")
    # Let's update the BLE Characteristic Value
    value=c.get_value()
    valueTime=cTime.get_value()
    print ("BLE input: ",value)
    print ("BLE Time input: ",valueTime)
    hardTimestamp = int(valueTime)
    intensity= 7*value+1200
    MyServo.moveToPulseWidth(intensity)
    print(MyServo.getCurrentPulseWidth())
    
    #Time Routines Module
    tm = rtc.get_utc()
    print("current_timestamp: ",tm.tv_seconds," hardData: ",hardTimestamp)
    print(tm.tm_year,'/',tm.tm_month,'/',tm.tm_mday,sep='')
    print(tm.tm_hour,':',tm.tm_min,':',tm.tm_sec,sep='')
    
    if(tm.tv_seconds >= hardTimestamp and tm.tv_seconds <= hardTimestamp + 2):
        print("Success on the interruption!")
        digitalWrite(2, HIGH)
    
    sleep(500)
