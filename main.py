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
import BerryComm
import Device

from wireless import wifi
from wireless import ble
from espressif.esp32ble import esp32ble as bledrv
from espressif.esp32net import esp32wifi as wifi_driver



streams.serial()


devices = []
devices.append(Device.Device(1,'Dimmer','DIMMABLE',D5.PWM))
#devices.append(Device. Device(2,'Dummy','ONOFF',D6 ))


def BerryParser(inputParser):
    #deviceId|dimmerValue|timestamp
    isDimmer = True
    splitRes = inputParser.split("|")
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


communication=BerryComm.BerryCommunication()

timestamp = -1
while(timestamp == -1):
    print("Trying to get timestamp")
    jsTimeRes = communication.GetCurrentTime()
    timestamp = int(jsTimeRes["unixtime"])
rtc.set_utc(timestamp)
()

TestIntensidad = 1000;
hardTimestamp = 0;
valueTime = "something"


while True:
    # Let's update the BLE Characteristic Value
    bleRawData=communication.BLE['Characteristics']['CurrentTime'].get_value()        #bleRawData=characteristic.get_value()
    print(bleRawData)
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
    
    sleep(10)

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



