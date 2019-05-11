from servo import servo 
import EnergySensor

class Device:

   
    
    def __init__(self, device_id, device_name, device_type,pin):
        
        self.device_id = device_id
        self.device_name= device_name
        self.device_type= device_type
        self.device_pin=  pin
        
        
        if device_type=='ONOFF':
            pinMode(self.device_pin,OUTPUT)
            self.off()
            
        if device_type == 'DIMMABLE':
            self.servo = servo.Servo(pin)
            self.servo.attach()
            self.off()
        
        if device_type =='ENERGYMSMNT':
            self.energy= EnergySensor.EnergySensor(pin,'H')
            ## Maybe here goes the start
    
           
        
    def set_intensity(self, intensity):
        if self.device_type== 'DIMMABLE':
            self.servo.moveToPulseWidth(8*intensity+1100)
        
    def on(self):
        if self.device_type== 'DIMMABLE':
            self.servo.moveToPulseWidth(1900)
        if self.device_type=='ONOFF':
            digitalWrite(self.device_pin,HIGH)
            
    def off(self):
        if self.device_type== 'DIMMABLE':
            self.servo.moveToPulseWidth(1100)
        if self.device_type=='ONOFF':
            digitalWrite(self.device_pin,LOW)
            
           



