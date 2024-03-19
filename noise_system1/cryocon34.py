#!/usr/bin/python

#import data_acquisition2.vxi_11 as vxi_11
import time,sys
from data_acquisition2.vxi_11 import vxi_11_connection                                                                                                        


class cryocon34(vxi_11_connection):
    def __init__(self,ipaddr='127.0.0.1', gpib=12,enable_selector=True):
        vxi_11_connection.__init__(self,host=ipaddr, device="gpib0,%s" % str(gpib), raise_on_err=1, timeout=1500,device_name="Cryo-Con 34")

    def abort(self):
        pass

    def send(self,string):
        self.write(string)

    def recv(self,timeout=None,count=None):
        return self.read(timeout=timeout,count=count)[2]

    def testF(self,string):
        self.write(string)
        
        tf=self.recv()
        return tf

    def get_tempK(self):
        self.write('INP A:TEMP?')
        tempK=self.recv()
#        return float(tempK.replace('+',''))
        return float(tempK)
    
    def get_heater(self):
        #get the temperature of internal heater circuitheat sink
        self.write('SYSTEM:HTRHST?')
        tempK=self.recv()
#        return float(tempK.replace('+',''))
        return str(tempK)

    def set_tempK(self,tempK):
        cmd="HEAT:SETP %s K" % str(tempK)
        self.write(cmd)
    #foo=self.recv()
        #self.write("cont")

    def wait_tempK(self,tempK):
        tempK=float(tempK)
        now=self.get_tempK()
        while abs(now-tempK)>0.2:
            time.sleep(4)
            now=self.get_tempK()
            print "Setting temperature: \ngoal: %s   now: %s   diff: %s" % (tempK,round(now,2) ,round(abs(now-tempK),2))

    def watch_tempK(self):
        start=time.time()
        while True:
            time.sleep(1)
            now=self.get_tempK()
            print "current: %s %s" % (time.time()-start,now)
            sys.stdout.flush()

    def reset(self):
        self.write("*RST")
        time.sleep(15)
        self.write("*CLS")
        #time.sleep(15)
        self.write('CONTROL')


if __name__=='__main__':
    tempcon=cryocon34('169.254.58.10',12)
    tempcon.write("*RST")
    print "Current Temperature",
    print tempcon.get_tempK()
    # get channal A temperature
    print "setting temperature"
    tempcon.set_tempK(320)
    print "watiing"
    tempcon.wait_tempK(320)
