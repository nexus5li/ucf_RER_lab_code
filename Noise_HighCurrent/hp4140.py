#!/usr/bin/python

import data_acquisition2.vxi_11 as vxi_11
import time,sys
from data_acquisition2.vxi_11 import vxi_11_connection


class hp4140(vxi_11_connection):
    def __init__(self,ipaddr='127.0.0.1', gpib=17,enable_selector=True):
	vxi_11_connection.__init__(self,host=ipaddr, device="gpib0,%s" % str(gpib), raise_on_err=1, timeout=1500,device_name="HP4140")

    def abort(self):
	pass

    def send(self,string):
	self.write(string)

    def recv(self,timeout=None,count=None):
	return self.read(timeout=timeout,count=count)[2]

    def set_reset(self):
	self.write("*RST\n")

    def set_voltA(self,voltage):
        cmd="A5L3PA%s\n" % voltage
	self.write(cmd)

    def set_voltB(self,voltage):
        cmd="B1M3PB%s\n" % voltage
	self.write(cmd)

    def set_output(self,state):
	if state==1:
    	    self.write('W1\n')
	if state==0:
	    self.write('W7\n')

if __name__=='__main__':
    voltsource=hp4140('169.254.58.10',17)
    voltsource.set_reset()
    voltsource.set_output(0)
    voltsource.set_voltA(1.1)
    voltsource.set_voltB(1.0)

#    voltsource.set_voltAB(1.4,2.2)
#    voltsource.set_output(1)
