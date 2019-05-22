import adc      # import the adc module  
import timers
import streams




class EnergySensor:
    


    def __init__(self, pin, samplingQ): 
        
         
        # Constantes propias del sensor 
        self.sensorSensibillity= 0.03727214522 # Sensibilidad en Voltios/Amperio para sensor de 30A
        self.sensorOffset= 1.465479666 # Constante del desface en voltios del sensor 
        self.boardMCompensation=0.92733312
        self.boardBCompensation= 0.1518599919
        # Variables del sensor
        self.inputPin= pin # Pin analogico de donde se tomará la medicion
        
        self.INow=0
        self.WNow=0
        # Variables de muestreo
        self.numSamplesAvg = 20 
        
        if(samplingQ == 'L'):
            self.samplesPerSecond = 1 # constante que indica la frecuencia de muestreo 
            self.interSampleTime= 325
        if(samplingQ == 'M'):
            self.samplesPerSecond = 2 # constante que indica la frecuencia de muestreo 
            self.interSampleTime= 300
        if(samplingQ == 'H'):
            self.samplesPerSecond = 3 # constante que indica la frecuencia de muestreo 
            self.interSampleTime= 280
            
        
        
        
        #Configuracion del sensor 
        pinMode(self.inputPin,INPUT_ANALOG)
        
        
    def calibrate(self,numSamples):
        avg=0
        for i in range(numSamples):
            avg =avg+ (((adc.read(self.inputPin)*(3.3 /4095.0))*self.boardMCompensation)+self.boardBCompensation)/numSamples
      
        avg=(abs(avg-self.sensorOffset))/self.sensorSensibillity
        
        wavg=avg*115
        print(avg,wavg)
        
        
        
        
    
    def start(self):

        while (True):
            IAvg=0
            lastTimeCalculated=0
            t = timers.timer()
            t.start()
            sampleCounter= self.samplesPerSecond
            while(sampleCounter>0):
                IValues = []
                elapsed = t.get()
                I=0
                while(t.get()-elapsed<=40):
                    sensorValue = adc.read(self.inputPin)  # Se obtiene la medicion del ADC
                    voltage = sensorValue * (3.3 / 4095.0)*self.boardMCompensation+self.boardBCompensation  # Se convierte el valor a voltaje y se deja como valor positivo
                    voltage=abs(voltage-self.sensorOffset)  # Se saca la diferencia respecto al valor de referencia del sensor
                    IValues.append((voltage)/self.sensorSensibillity)  # Se convierte a corriente y se guarda en el arreglo temporal
                    sleep(1)  # We meess with time.
            
                dt=t.get() - lastTimeCalculated
                lastTimeCalculated=t.get()
                for i in range(39):
                    I=I + IValues.pop()
                I=I/39
                
                #1.11058749  Factor AVG RMS
                IAvg=IAvg+I/self.samplesPerSecond
                IAvg=IAvg* 1.11058749
                sleep(self.interSampleTime)
                sampleCounter= sampleCounter-1 
              
            
            print("Time:",t.get()," I: ",IAvg," W: ", IAvg*115 )  #Debug
            IAvg=0 #Se resetea la corriente de cada segundo
            t.reset()    
         
       
         
        
        
        
        
        
        
        
        
        
      #  for i in range(self.samplesPerSecond*60):
        
       #     for i in range(self.numSamplesAvg):
                
                
                
        #    self.Irms[i]= max(IValues) * 0.707
            
         #   sleep(1000/self.samplesPerSecond - self.numSamplesAvg)
           
            
           
        
        






        