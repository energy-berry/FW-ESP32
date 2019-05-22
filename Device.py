from servo import servo 
import EnergySensor

class Device:
    
    def __init__(self, device_id, device_name, device_type,pin):
        
        self.taskList = []
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
        self.taskList.append(task)
        
    
        
    
    def execute_tasks(self, berryTime):
        print("Device ", self.device_name ," Number of tasks: ",len(self.taskList))
        counter = 0;
        taskToRemove = []
        
        for task in self.taskList:
            exeTask = False
            if('NOW' in task['timestamp']):
                exeTask = True
                taskToRemove.append(counter)
            elif(berryTime >= int(task['timestamp']) and berryTime <= int(task['timestamp']) + 2):
                exeTask = True
                taskToRemove.append(counter)
            if exeTask:
                print("Executing task on Device: ", self.device_name)
                if task['value'] == 'ON':
                    self.on()     
                elif task['value'] == 'OFF':
                    self.off()
                else:
                    self.set_intensity(int(task['value']))
            counter= counter+1
        
        for idxToRemove in taskToRemove:
            del self.taskList[idxToRemove]
