from data_acquisition import vxi_11
from data_acquisition.vxi_11 import vxi_11_connection
import sys

class VoltageSupply(vxi_11.vxi_11_connection):
    def __init__(self,host='169.254.7.112', gpib=24,enable_selector=True):
	vxi_11_connection.__init__(self,host=host, device="gpib0,%s" % str(gpib), raise_on_err=1, timeout=15000,device_name="voltage supply")
    def abort(self):
	pass

    def set_voltage_b(self,voltage):
    	self.write(':output off')
    	self.write(":sense:func 'curr'")
    	self.write(':source:volt 0.0')
    	self.write(':SOUR:DEL:AUTO ON')
    	self.write(':format:data ASCII')
    	self.write(':sense:current:prot 0.1')
    	self.write(':TRACe:cle')
    	self.write(':trig:coun 1')
    	self.write(':output on')
    	self.write(':source:volt %s' %str(voltage))

if __name__=='__main__':
    ps=VoltageSupply()
    ps.set_voltage_B(0.0)


