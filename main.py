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
devices.append(Device.Device('1','Dimmer','DIMMABLE',D5.PWM))
devices.append(Device. Device('2','Relev1','ONOFF',D6 ))
devices.append(Device. Device('3','Relev2','ONOFF',D7 ))


def BerryParser(inputParser):
    
    #deviceId|dimmerValue|timestamp
    splitRes = inputParser.split("|")
    devices[splitRes[0]].add_task(splitRes[1],splitRes[2])

communication=BerryComm.BerryCommunication()

timestamp = -1
while(timestamp == -1):
    print("Trying to get timestamp")
    jsTimeRes = communication.GetCurrentTime()
    timestamp = int(jsTimeRes["unixtime"])
rtc.set_utc(timestamp)


#### BERRY ENERGYMSMNT THREAT


#### BERRY'S MAIN LOOP
while True:
    # 1- CHECKING FOR INCOMING STRUCTIONS FROM BLE
    bleInput=communication.BLE['Characteristics']['CurrentTime'].get_value()
    seperator = ''
    bleInput=seperator.join(bleInput)
    print("(", bleInput, ")") #TEST PRINTt
    
    # 2- SENDING INSTRUCTIONS TO THE DEVICES
    if(bleInput != ""): #CHECKING FOR CHANGES = "" -> None
        device = BerryParser(bleInput)
    
    # 3- POLING THE DEVICES FOR PENDING TASKS AND RUN THEM
    for dev in devices:
        espTime = rtc.get_utc()
        dev.execute_tasks(espTime.tv_seconds)
    
    sleep(10)