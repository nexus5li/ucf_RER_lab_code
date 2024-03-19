#!/usr/bin/python
import e5810
import random


class Multimeter:
    def __init__(self,IPADDR='129.59.140.97',PAD=19,DEVNAME='multimeter',sim=False):
	self.Simulate=sim
	self.IPADDR=IPADDR
	self.PAD=PAD
	self.DEVNAME=DEVNAME
	if self.Simulate==False:
	    self.handle=e5810.e5810(host=self.IPADDR,device="gpib0,%s" % str(self.PAD),raise_on_err=0,timeout=5000,device_name=self.DEVNAME)

    def read_voltage(self):
	if self.Simulate==True:
	    return(random.random()) 
	self.handle.write("F1R-2RAN5T1Z0D1") 
	volt=float(self.handle.read()[2])
	return volt

