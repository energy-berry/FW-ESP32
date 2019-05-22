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
import EnergySensor

from wireless import wifi 
from wireless import ble
from espressif.esp32ble import esp32ble as bledrv
from espressif.esp32net import esp32wifi as wifi_driver
streams.serial()


devices = []
devices.append(Device.Device('0','Dimmer','DIMMABLE',D5.PWM))
devices.append(Device. Device('1','Relev1','ONOFF',D2 ))
devices.append(Device. Device('2','Relev2','ONOFF',D4 ))
#devices.append(Device.Device('3','Energy','ENERGYMSMNT',A0))
print("Devices Created Done")

communication=BerryComm.BerryCommunication()
print("Communication Created Done")

timestamp = -1
while(timestamp == -1):
    print("Trying to get timestamp")
    timestamp = communication.GetCurrentTime()
rtc.set_utc(timestamp)
print("World timestamp Done")


while True:
    
    print("STEP 0: CHECKING BLE")
    # 1- CHECKING FOR INCOMING STRUCTIONS FROM BLE
    print("STEP 1: CHECKING BLE")
    bleInput=communication.BLE['Characteristics']['CurrentTime'].get_value()
    
    #stringInput = ''.join(bleInput)
    stringInput = bleInput.strip()
    stringInput = stringInput.replace('\0', '')
    stringInput = stringInput.replace(' ', '')
    isValid = '|' in stringInput
    print("(", stringInput, ")  is Valid: ", isValid)
    
    # 2- SENDING INSTRUCTIONS TO THE DEVICES
    print("STEP 2: SENDING INSTRUCTIONS")
    if(isValid): #CHECKING FOR CHANGES  "" -> None
        #deviceId|dimmerValue|timestamp
        print(">", stringInput, "<")
        splitRes = stringInput.split("|")
        print("num items: ",len(splitRes))
        
        devices[int(splitRes[0])].add_task(splitRes[1],splitRes[2])
    
    # 3- POLING THE DEVICES FOR PENDING TASKS AND RUN THEM
    print("STEP 3: POLING DEVICES")
    for dev in devices:
        espTime = rtc.get_utc()
        dev.execute_tasks(espTime.tv_seconds)
    #print(".")
    sleep(500)