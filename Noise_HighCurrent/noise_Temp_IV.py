
#!/usr/bin/python

# this file is used for off-site test, please change T-start and T-end
import k2410
import numpy as np
import csv
import time
import os

import sys

import os

import subprocess

sys.path.append('./modules/')

#import data_acquisition2.vxi_11 as vxi_11

import time

import math

from data_acquisition2.vxi_11 import vxi_11_connection

import cryocon34

import hp4140

import voltage_supply

import voltage_supply2

import multimeter

import hp3478

import os


Simulate=False

e5810_addr='10.8.129.29'
#e5810_addr='10.8.129.254'
#e5810_addr='169.254.58.10'
#tstart=300
#tend=300
tstart=300
tend=380
#e5810_addr='169.254.58.10'
#increment= 2.68654
#print "increment=",increment



SA=sr760.sr760(e5810_addr,10)

tempcon=cryocon34.cryocon34(e5810_addr,12)

automeasure=1 # set 1 for default settings, 0 to start input

##increment=-0.6 # Vgate-Vth

##tstart=100

##tend

Tempcontrol=0

while temperature <= tend:
# cryostat settings
#    tempcon.write("*RST")
    print "Reset"
#    time.sleep(14)
    print "sending Signal..."
#    tempcon.write("*CLS")
    time.sleep(4)
    print "Connected!!\nCurrent Temperature"
    print tempcon.get_tempK()
    tempcon.write('HEAT:RANGE HI')
    # set power: HI,MID,LOW
    tempcon.write('CONTROL')

#if (Tempcontrol==1):
# temperature control
    print "Current Temperature",
    print tempcon.get_tempK()
    print "setting temperature"
    tempcon.set_tempK(temperature)


    tempcon.wait_tempK(temperature)

    print "Temperature goal achieved: %s K \n" % temperature
    print "Wait 150 seconds...\n"
    time.sleep(150)    #high speed 90s,DIP 120-150s

    temperature=temperature+5

if (temperature>270):
	temperature=300
	#    tempcon.write("*RST")
	print "Current Temperature",
	print tempcon.get_tempK()
	print "setting temperature"
	tempcon.set_tempK(temperature)
	print "waiting"
	tempcon.wait_tempK(temperature)

print "Temperature goal achieved: %s K \n" % temperature
print "Finished \n"



