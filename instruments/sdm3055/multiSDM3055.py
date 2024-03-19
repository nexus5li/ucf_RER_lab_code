from pymeasure.instruments import Instrument

class multiSDM3055(Instrument):
    def read_DC_voltage(self):
        self.write("CONF:VOLT:DC")
        self.write("VOLT:DC:NPLC 10")
        self.write("TRIG:SOUR IMM")
        self.write('MEAS:VOLT:DC?')
        voltage = self.values('READ?')[0]
        return voltage
    
    #----Sampling read the measured data------*
    def sampling_voltage(self, sample_number:int,trigger_time:int):
        self.write("CONF:VOLT:DC")
        self.write("VOLT:DC:NPLC 10")
        self.write("TRIG:SOUR IMM")
        self.write(f"TRIG:COUN {trigger_time}")
        self.write(f"SAMP:COUN {sample_number}")
        
        wait_time = 1 * sample_number * trigger_time
        self.wait_for(wait_time)
        voltages = self.values('READ?')
        return voltages
    
    def read_AC_voltage(self):
        self.write("CONF:VOLT:AC")
        self.write("TRIG:SOUR AUTO")
        self.write('MEAS:VOLT:AC?')
        voltage = self.values('READ?')[0]
        return voltage
    