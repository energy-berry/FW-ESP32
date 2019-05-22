import streams
import json
import requests
from wireless import ble
from espressif.esp32ble import esp32ble as bledrv

from wireless import wifi
from espressif.esp32net import esp32wifi as wifi_driver
from googlecloud.iot import iot
import helpers


# Imports necesary resources 
new_resource('private.hex.key')
new_resource('GCPdevice.conf.json')

streams.serial()
#Initializea a GCP device
def init_GCP_device():
    pkey = helpers.load_key('private.hex.key')
    device_conf = helpers.load_device_conf()
    publish_period = 1000
    device = iot.Device(device_conf['project_id'], device_conf['cloud_region'], device_conf['registry_id'], device_conf['device_id'], pkey, get_timestamp)
    device.mqtt.connect()
    device.on_config(config_callback)
    device.mqtt.loop()
    return device

# Gets a timestamp 
def get_timestamp():
    user_agent = {"user-agent": "curl/7.56.0"}
    return json.loads(requests.get('http://now.zerynth.com/', headers=user_agent).content)['now']['epoch']
    

# define a callback for config updates
def config_callback(config):
    global publish_period
    print('requested publish period:', config['publish_period'])
    publish_period = config['publish_period']
    return {'publish_period': publish_period}



def initBLE():
    bledrv.init()
    # Set GAP name
    ble.gap("Enegy Berry Module")
    
    
    # Create Real Time Clock GATT Service an Characteristic
    time_service = ble.Service(0x1805)
    time_char = ble.Characteristic(0x2A2B,ble.NOTIFY | ble.READ | ble.WRITE,20,"Current Time",ble.STRING)
    time_service.add_characteristic(time_char)
    ble.add_service(time_service)
    
    # Create Battery Level GATT Service an Characteristic
    battery_service = ble.Service(0x180F)
    battery_char = ble.Characteristic(0x2A58,ble.NOTIFY | ble.READ | ble.WRITE,1,"Battery Level",ble.NUMBER)
    battery_service.add_characteristic(battery_char)
    ble.add_service(battery_service)
    
    # Start the BLE stack
    ble.start()
    ble.start_advertising()
    #ct.set_value("")
    
    BLE={
        'Services': 
        {
            'CurrentTime': time_service,
            'BatteryLevel': battery_service
        },
        
        
        'Characteristics':
        {
            'CurrentTime': time_char,
            'BatteryLevel': battery_char
        }
    }
    
    
    return BLE 


class BerryCommunication:
    #Initializing of the Comunication module
    def __init__(self):
    
        # Inits WIFI driver and connects to the wifi access point
        wifi_driver.auto_init()
        try:
            print("tratando de establecer la conexion WIFI...")
            wifi.link("AXTEL-2765",wifi.WIFI_WPA2,"B4742765") #HOME-2508 / 415CF0870ADC04E2
            print("WIFI conectado!")
        except Exception as e:
            print("No se pudo establecer la conexion WIFI: ",e)
            
            
        # Inits the gcp device
        print("iniciando GCP...")
        self.GCP_device = init_GCP_device()
        
        # Inits the BLE service
        print("iniciando servicio BLE...")
        self.BLE=initBLE()
        
    
    
    def GCP_publish (self, device_status):
        self.GCP_device.publish_event(device_status)
        
        
    def GetCurrentTime(self):
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
            return js["unixtime"]  
        except Exception as e:
            print("ooops, something very wrong! :(",e)
            return -1
