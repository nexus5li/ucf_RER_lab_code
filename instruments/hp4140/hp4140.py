from pymeasure.instruments import Instrument
from pymeasure.adapters import VXI11Adapter

class hp4140(Instrument):
    def set_voltage_a(self, gate_voltage):
        self.write("W3") #PAUSE
        self.write("A5") #DC output
        self.write("L2") # Channel A 10mA limit
        self.write(f'PA{gate_voltage};') #set gate voltage
        self.write("W4") #RESTART
    
    def set_voltage_b(self,drain_voltage): #FOR SYSTEM 2
        self.write("W7") #reset
        self.write("RA1") #autorange
        self.write("B1") #Channel B on in DC output
        self.write("M3") #Channel B 10mA limit
        self.write(f'PB{drain_voltage};') #set drain voltage
        self.write("W1")
        
    def reset(self):
        self.write('W7')
        self.write('A5') #Output A in DC mode
        self.write('B1') #Output B in DC mode
        self.write('PA0.0;') #set Output A voltage to 0
        self.write('PB0.0;')#set Output A voltage to 0
