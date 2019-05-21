from servo import servo 
import EnergySensor

class Device:
    
    taskList = []
    ##EXAMPLE task item =========
    #task = {
    #        'value': "100" ,
    #        'timestamp': "-1",
    #    }
        
    #taskList.append(task)
    ## ==========================
    
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
            
    def add_task(self, val, time):
        task = {
            'value': val ,
            'timestamp': time,
        }
        taskList.append(task)
    
    def execute_tasks(self, berryTime):
        for task in taskList:
            if(berryTime >= task['timestamp'] and berryTime <= task['timestamp'] + 2) or task['timestamp'] == 'Now'):
                print("Executing task on Device: ", device_name)
                if(task['value'] == "On"):
                    on()     
                elif(task['value'] == "Off"):
                    off()
                else
                    set_intensity(int(task['value']))