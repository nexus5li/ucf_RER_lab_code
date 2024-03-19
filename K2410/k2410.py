from pymeasure.instruments import Instrument
from pymeasure.adapters import VXI11Adapter
from pymeasure.instruments.keithley import Keithley2400
import time

class keithley2410(Keithley2400):
    
    def abort(self):
        pass

    def output_switch(self,status):
        self.write(f':output {status}')
        
    def measure_fuction(self,mode):
        self.write(f":sense:func: '{mode}'")
        
    def source_delay(self, delay_time):
        self.write(f':source:delay {delay_time}')
        
    def format_data(self,mode):
        self.write(f':format:data {mode}')
        
    def set_compliance(self,compliance):
        self.write(f':sense:current:prot {compliance}')
        
    def set_null_feed(self,mode):
        self.write(f':calculate2:null:state {mode}')
        
    def set_voltage(self,voltage):
        self.write(f":source:volt {voltage}")
        
    def read_data(self):
        self.write('Trace:DATA?')
    def read(self):
        self.read()
        
    
        
        

        