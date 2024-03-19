#!/usr/bin/python
import data_acquisition2.vxi_11 as vxi_11
import time

class e5810(vxi_11.vxi_11_connection):
    def abort(self):
	pass

    def write(self,string):
	a=vxi_11.vxi_11_connection.write(self,string)
	err,sb=self.read_status_byte()
