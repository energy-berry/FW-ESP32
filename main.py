################################################################################
# BLE Battery Service 
#
# Created by Zerynth Team 2016 CC
# Author: G. Baldi
###############################################################################

import streams
# import a BLE driver: in this example we use NRF52
#from nordic.nrf52_ble import nrf52_ble as bledrv
# then import the BLE modue
#from wireless import ble
#import the ESP32 BLE driver: a BLE capable VM is also needed!
from espressif.esp32ble import esp32ble as bledrv
# then import the BLE modue
from wireless import ble

from servo import servo

streams.serial()

MyServo=servo.Servo(D5.PWM)

# initialize NRF52 driver
bledrv.init()

# Set GAP name
ble.gap("Berry dimmer")

# Create a GATT Service: let's try a Battery Service (uuid is 0x180F)
s = ble.Service(0x180F)

# Create a GATT Characteristic: (uuid for Battery Level is 0x2A19, and it is an 8-bit number)
c = ble.Characteristic(0x2A19,ble.NOTIFY | ble.READ | ble.WRITE,1,"Battery Level",ble.NUMBER)

# Add the GATT Characteristic to the Service
s.add_characteristic(c)

# Add the Service
ble.add_service(s)

# Start the BLE stack
ble.start()

# Begin advertising
ble.start_advertising()

c.set_value(0)

MyServo.attach()
while True:
    print(".")
   
    value=c.get_value()
    
    
    # Let's update the Characteristic Value
    print (value)
    i= 7*value+1200
    MyServo.moveToPulseWidth(i)
    print(MyServo.getCurrentPulseWidth())
    #c.set_value(value)
    sleep(500)
    #MyServo.detach()
