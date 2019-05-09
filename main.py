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

devices = {
    "1" : Device(1),
    "2" : Device(2)
}

devices = [Device(1), Device(2)]

class Device:

    timestamp = -1
    dimmerValue = 0
    intensity = 0
    
    def __init__(self, idDev,isDimmable):
        self.dimmable = isDimmable
        self.id = idDev
        if(isDimmable):
            self.servo = servo.Servo(D5.PWM)
            self.servo.attach()
        else:
            pinMode(id,OUTPUT)

    def setDimmerInfo(self,dimVal, timeStmp):
        self.dimmerValue = dimVal
        self.timestamp = timeStmp
        self.intensity = 8*dimVal+1100

    def setIntensity(self):
        if(isDimmable):
            self.servo.moveToPulseWidth(intensity)
        else:
            digitalWrite(self.id, HIGH if self.dimmerValue == 100 else LOW)


def initBLE():
    bledrv.init()
    # Set GAP name
    ble.gap("Enegy Berry Module")
    # Create a GATT Service
    service = ble.Service(0x1805)
    # Create a GATT Characteristic
    characteristic = ble.Characteristic(0x2A2B,ble.NOTIFY | ble.READ | ble.WRITE,20,"Current Time",ble.STRING)
    # Add the GATT Characteristic to the Service
    service.add_characteristic(characteristic)
    ble.add_service(service)
    # Start the BLE stack
    ble.start()
    ble.start_advertising()
    characteristic.set_value("")

def BerryParser(inputParser):
    #deviceId|dimmerValue|timestamp
    isDimmer = True
    splitRes = text.split("|")
    if(splitRes[1] == "On"):
        splitRes[1] = 100
        isDimmer = False
    if(splitRes[1] == "Off"):
        splitRes[1] = 0
        isDimmer = False
    if(splitRes[2] == "Now"):
        splitRes[2] = -1
        
    device = devices[splitRes[0]]
    device.dimmable = isDimmer
    device.setDimmerInfo(splitRes[1], splitRes[2])

    return device


def GetCurrentTime():
    wifi_driver.auto_init()
    # use the wifi interface to link to the Access Point
    # change network name, security and password as needed
    print("Establishing Link...")
    try:
        # FOR THIS EXAMPLE TO WORK, "Network-Name" AND "Wifi-Password" MUST BE SET
        # TO MATCH YOUR ACTUAL NETWORK CONFIGURATION
        wifi.link("HWAV",wifi.WIFI_WPA2,"2019hwav")
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
rtc.set_utc(timestamp)
#===================  BLE INIT
initBLE()

TestIntensidad = 1000;
hardTimestamp = 0;
valueTime = "something"

while True:
    print(".")
    # Let's update the BLE Characteristic Value
    bleRawData=characteristic.get_value()
    seperator = ''
    bleRawData=seperator.join(bleRawData)
    print ("BLE Raw input: (", bleRawData, ")")
    
    device = BerryParser(bleRawData)
    device.setIntensity()
   
    #valueTime=str(valueTime)
    #print ("BLE Splited input: (", bleDataArray, ")")
    #if valueTime[0] != '\0':
    #    hardTimestamp = int(valueTime)
    #    hardTimestamp = int(hardTimestamp/1000)
    
    
    #Time Routines Module
    espTime = rtc.get_utc()
    #print("current_timestamp: ",.tv_seconds," hardData: ",hardTimestamp)
    #print(espTime.tm_year,'/',espTime.tm_month,'/',espTime.tm_mday,sep='')
    #print(espTime.tm_hour,':',espTime.tm_min,':',espTime.tm_sec,sep='')
    
    if(espTime.tv_seconds >= hardTimestamp and espTime.tv_seconds <= hardTimestamp + 2):
        print("Success on the interruption!")
        digitalWrite(2, HIGH)
        TestIntensidad = 1900
    
    sleep(1)

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