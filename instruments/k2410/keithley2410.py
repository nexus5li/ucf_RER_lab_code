from pymeasure.instruments import Instrument
from pymeasure.adapters import VXI11Adapter
from pymeasure.instruments.keithley import Keithley2400

class keithley2410(Keithley2400):

    def __init__(self, adapter, data_format='ASCII', compliance_current=1e-3, compliance_voltage = 1e2, **kwargs):
        super().__init__(adapter, **kwargs)
        self.data_format = data_format
        self.compliance_current = compliance_current
        self.compliance_voltage = compliance_voltage
    
    # Customized method based on legacy python2 code
    def output_switch(self,status):
        self.write(f':output {status}')
        
    def measure_fuction(self,mode):
        self.write(f":sense:func: '{mode}'")
        
    def source_delay(self, delay_time):
        self.write(f':source:delay {delay_time}')
        
    def format_data(self):
        self.write(f':format:data {self.data_format}')
        
    def set_compliance(self,compliance):
        self.write(f':sense:current:prot {compliance}')
        
    def set_null_feed(self,mode):
        self.write(f':calculate2:null:state {mode}')
        
    def set_voltage(self,voltage):
        self.write(f":source:volt {voltage}")
        
    def read_data(self):
        self.write('Trace:DATA?')
        
    # def read(self):
    #     self.read()

    def read_voltage(self):
        self.enable_source()
        self.measure_voltage()
        voltage = self.voltage
        return voltage


    def smu_initialization_voltage(self, source_delay='5e-1'):
        self.disable_source()
        self.apply_voltage(compliance_current=self.compliance_current)
        self.source_delay(source_delay)
        self.format_data()
        self.set_null_feed('ON')
        self.source_voltage = 0

    
    def reset_and_set_voltage(self, voltage_value):
        self.disable_source()
        self.measure_current()
        self.source_voltage = 0
        self.source_delay_auto = True
        self.format_data()
        self.write(':TRACe:cle')
        self.apply_voltage(compliance_current=self.compliance_current)
        self.trigger_count = 1
        self.enable_source()
        self.source_voltage = voltage_value
    
    def smu_initialization_current(self, source_delay = '5e-1'):
        self.disable_source()
        self.apply_current(compliance_voltage=self.compliance_current)
        self.source_delay(source_delay)
        self.format_data()
        self.set_null_feed('ON')
        self.source_current = 0
    
    def reset_and_set_current(self, current_value):
        self.disable_source()
        self.measure_voltage()
        self.source_current = 0
        self.source_delay_auto = True
        self.format_data()
        self.write(':TRACe:cle')
        self.apply_current(compliance_voltage=self.compliance_voltage)
        self.trigger_count = 1
        self.enable_source()
        self.source_current = current_value

