#!/usr/bin/python

#TODO:
#1. Check if possible to program amplification factor of preamp automatically


import sys
import time, os, math, numpy
import cryocon34
import voltage_supply
import mult_34460
import hp3562
import sr760
import matplotlib.pyplot as plt
import datetime
from setup_drain_voltage import setup_drain_voltage
import csv
import numpy as np
import numpy.polynomial.polynomial as poly

# ------> NETWORK CONFIGURATION <-----
e5810_addr='10.8.129.29'
# e5810_addr='129.59.93.192'
#e5810_addr='129.59.93.192'
#setup_2_ip = '129.59.93.105'


#voltsource=voltage_supply.VoltageSupply(e5810_addr,17)
# voltsource=voltage_supply.VoltageSupply(e5810_addr,15)
voltsource=voltage_supply.VoltageSupply(e5810_addr,15)
#voltsource_2=voltage_supply.VoltageSupply(setup_2_ip,15)  #for bias on bulk
meter=mult_34460.mult_34460(e5810_addr,23)
#spA=hp3562.hp3562(e5810_addr,10)
tempcon=cryocon34.cryocon34(e5810_addr,12)
spA=sr760.sr760(e5810_addr,10)

# ---> PARAMETERS <-----
date = datetime.date.today() #today's date for naming output files
deviceName = 'TEST' #device identificator for  naming output files
deviceName = 'GaAs_HEMTs' #device identificator for  naming output files
# path = 'd:\#Research\Tools\Python\code\Noise\'
numbAve=5000 #!5000-6000 or 8000 if noise data are not good for SR760
numbAve_bg = 4000 #for SR760
#numbAve = 50 # for HP3562A
#numbAve_bg = 25 # averaging for background noise for HP3562A
amplFact = 200 #!check preamplifier
spAn_array = [11] #for 400 Hz
# tstart = 300
# tend = 300
# temperature = 300
tstart = 170
tend = 260
temperature = tstart
Vb_array = [0]
#Vb_array = [0, -2]
Vd_array = [0.05]
#Vd_array = [0.03, 0.05, 0.1]
Vgt_array=[0.25]
# Vgt_array=[0.4, 0.1, 0.2, 0.3, 0.5, 0.6]
#service variable
vd_measd = 0

#Vt_values = [-0.358,-0.388,-0.406]
#T_values =  [80,140,170]
Vt_values = [-0.406,-0.452,-0.506]
T_values =  [170,200,260]
#Vt_values = [-0.508,-0.543,-0.562]
#T_values =  [260,320,380]

def convToSv(amplFact,fg_spectrum,bg_spectrum):
    noiseArr=[]
    fdataArr=[]
    bdataArr=[]
    for fgdata,bgdata in zip(fg_spectrum,bg_spectrum):
        fdata=fgdata/amplFact
        bdata=bgdata/amplFact
        noise=fdata*fdata-bdata*bdata 
        noiseArr.append(noise)
        fdataArr.append(fdata*fdata)
        bdataArr.append(bdata*bdata)
    return((noiseArr,fdataArr,bdataArr))



#---------------Vth(T) calculation--------------
new_T = np.linspace(T_values[0], T_values[-1], num=91) #num=(max-min)/step+1
coef_Vt = poly.polyfit(T_values, Vt_values, 2)
ffit_Vt = poly.polyval(new_T,coef_Vt)

c = np.array([new_T, ffit_Vt]).T

# -----> MAIN <-----
print 'MAIN: Starting the test...'
print 'Temperature controller: Resetting...'
tempcon.reset()
print 'OK'
while temperature <= tend:
    #---------> SETTING TEMPERATURE <-------
    print "Temperature controller: Current Temperature = ", round(tempcon.get_tempK(),2)
    print "Temperature controller: Setting temperature..."
    tempcon.set_tempK(temperature)
    tempcon.wait_tempK(temperature)
    print "Temperature controller: Goal temperature achieved: %s K \n" % round(tempcon.get_tempK(),2)
    print "Wait 55 seconds...",
    time.sleep(55)
    print "OK"
    print "Temperature controller: Actual temperature: %s K \n" % round(tempcon.get_tempK(),2)
    # ------------------- Vth adjustment --------------
    Vth_T = c[(c[:, 0] == temperature), 1]

    for freqspAn in spAn_array:
        for Vb in Vb_array:
            #print 'MAIN: Starting the test for Vb = %s' % (Vb)
            for Vd in Vd_array:
                #print 'MAIN: Starting the test for Vd = %s' % (Vd)
                for Vgt in Vgt_array:
                    Vg_cur = Vgt + Vth_T[0]
                    print 'MAIN: Starting the test for Vgt = %s' % (Vgt)
                    voltsource.reset()
                    voltsource.set_voltage_b(0)
                    # voltsource_2.reset()
                    # voltsource_2.set_voltage_a(Vb)  # set voltage on B
                    print 'Temperature = %s \nVth(T) = %s \nVg_cur = %s' % (temperature, (round(Vth_T[0], 4)), round(Vg_cur,4))
                    voltsource.set_voltage_a(Vgt + Vth_T[0])  # set voltage on G

                    print "Supply: Setup for background measurement...",
                    voltsource.set_voltage_b(0)  # drain to zero
                    # spA.reset()
                    # spA.setupNoise(numbAve_bg, freqspAn)
                    spA.setup(numbAve_bg, freqspAn)  # 760
                    print "OK"
                    print "Wait 20 seconds...",
                    time.sleep(20)
                    print "OK"

                    print "Temperature controller: Actual temperature: %s K " % round(tempcon.get_tempK(), 2)
                    tempcon.wait_tempK(temperature)
                    print "Temperature controller: Temperature achieved: %s K \n" % tempcon.get_tempK()

                    print "Spectrum An.: Background measurement...",
                    spA.start()
                    spA.wait()
                    print "OK"

                    print "Spectrum An.: Downloading background data...",
                    time.sleep(1.5)
                    fb_array, bg_array = spA.read_spectrum()
                    if len(fb_array) == 0:
                        time.sleep(5)
                        fb_array, bg_array = spA.read_spectrum()
                    print "OK"

                    print 'Supply: Setting drain voltage...'
                    setup_drain_voltage(Vd=Vd, Vd_delta=0.001, set_sup_Vd=voltsource.set_voltage_b, measure_Vd=meter.read_voltage, max_steps=5, dbg=True)
                    print 'OK'

                    print "Spectrum An.: Setting up for noise measurements",
                    # spA.reset()
                    # spA.setupNoise(numbAve,freqspAn)
                    spA.setup(numbAve,freqspAn) #760
                    print "OK"
                    print "Wait 25 seconds...",
                    time.sleep(25)
                    print "OK"

                    vd_measd = meter.read_voltage()
                    print 'Multimeter: Check Vd set = ', round(vd_measd, 4)
                    
                    print "Temperature controller: Actual temperature: %s K " % round(tempcon.get_tempK(), 2)
                    tempcon.wait_tempK(temperature)
                    print "Temperature controller: Temperature achieved: %s K \n" % tempcon.get_tempK()
                    
                    print "Spectrum An.: Spectra measurement...",
                    spA.start()
                    spA.wait()
                    print "OK"

                    voltsource.set_voltage_a(0)  # gate to zero
                    voltsource.set_voltage_b(0)  # drain to zero
                    #voltsource_2.set_voltage_a(0)  # back gate bias to zero

                    print "Spectrum An.: Downloading data...",
                    time.sleep(1.5)
                    f_array, fn_array = spA.read_spectrum()
                    if len(f_array) == 0:
                        time.sleep(5)
                        f_array, fn_array = spA.read_spectrum()
                    print "OK"

                    print "MAIN: Converting data...",
                    noiseSv,fdata,bdata=convToSv(amplFact,fn_array,bg_array)
                    print "OK"

                    print "MAIN: Saving data...",
                    deviceinfo='%s_%s_Vgt=%s_Vd=%s_Vb=%s_T=%s' % (date,deviceName,Vgt,vd_measd, Vb, temperature)
                    ff=open('%s.txt' % deviceinfo,'w')
                    for c1,c2,c3,c4 in zip(fb_array,noiseSv,fdata,bdata):
                        ff.write('%s %s %s %s\n' % (c1,c2,c3,c4))
                    ff.close()
                    print "OK"
                    

                    print "MAIN: Plotting data...",
                    plt.scatter(fb_array, noiseSv)
                    plt.scatter(fb_array, bdata)
                    plt.xscale('log')
                    plt.yscale('log')
                    plt.ylim([1e-17, 1e-7])
                    plt.xlim([0.5, 1000])
                    plt.xlabel('f (Hz)')
                    plt.ylabel('Svd(V^2/HZ)')
                    plt.savefig('%s.png' %deviceinfo)
                    print "OK"
                    print "MAIN: Test Vgt=%s is finished for Vd = %s and T = %s" % (Vgt, Vd, temperature)
    temperature = temperature + 5
# voltsource.reset()
tempcon.reset()
# voltsource  _2.reset()
