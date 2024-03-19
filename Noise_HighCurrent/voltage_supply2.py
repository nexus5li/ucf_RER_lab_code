#!/usr/bin/python
import e5810


class VoltageSupply:
    def __init__(self,IPADDR='129.59.140.97',PAD=16,DEVNAME='voltage supply',sim=False):
	self.Simulate=sim
	self.IPADDR=IPADDR
	self.PAD=PAD
	self.DEVNAME=DEVNAME
	if self.Simulate==False:
	    self.handle=e5810.e5810(host=self.IPADDR,device="gpib0,%s" % str(self.PAD),raise_on_err=0,timeout=5000,device_name=self.DEVNAME)

    def set_voltage_a(self,voltage=0.0):
	if self.Simulate==True:
	    return True
	self.handle.write("W7") #;//reset/abord
        self.handle.write("A5,L3,PA%s;" % str(voltage))
	self.handle.write("W1")
	return True

    def set_voltage_b(self,voltage=0.0):
	if self.Simulate==True:
	    return True
	self.handle.write("W7;RA1;B1;M3;")
	self.handle.write("PB%s;" % str(voltage))
	self.handle.write("W1")
	return True



if __name__=='__main__':
    ps=VoltageSupply()
    ps.set_voltage_A(0.0)
    ps.set_voltage_B(0.0)
    

