#python d:\#Research\Tools\Python\code\python\data\noise_wo_temp.py
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

#import data_acquisition.vxi_11 as vxi_11

import time

import math

from data_acquisition.vxi_11 import vxi_11_connection

import cryocon34

import hp4140


import voltage_supply

import voltage_supply2

import multimeter

import hp3478


import sr760

#import Gnuplot

import scipy.stats

import os



Simulate=False#

e5810_addr='129.59.93.105'

#e5810_addr='169.254.58.10'

temperature=300

vdrain=1
Vgate=0
vsupply=0

#e5810_addr='169.254.58.10'
#increment= 2.68654

#print "increment=",increment
#os.chdir('/Users/panwang/GoogleDrive/data/version2/Moisture/sample1/sample1B2/Gate')
#os.chdir('/Users/panwang/Desktop/cern/Day1_highT1h/G2')


#os.chdir('/Users/panwang/GoogleDrive/data/grapheneFET/switchbias/19nmI3+5V_100K')

#os.chdir('/Users/panwang/GoogleDrive/data/anothergraphene/gatedep/unpass/E3')
#os.chdir('/Users/panwang/GoogleDrive/graphene')
#zos.chdir('d:\#Research\SOI_FinFETs\Noise_data')
os.chdir('/Users/wangpengfei/Desktop/TestData')


#voltsource=voltage_supply.VoltageSupply(e5810_addr,gpib=24)
#voltsource2=voltage_supply2.VoltageSupply(e5810_addr,PAD=15,DEVNAME='voltage supply',sim=Simulate)

#meter=multimeter.Multimeter(e5810_addr,PAD=18,DEVNAME='multimeter',sim=Simulate)

SA=sr760.sr760(e5810_addr,10)

tempcon=cryocon34.cryocon34(e5810_addr,12)



automeasure=1 # set 1 for default settings (for names), 0 to start input

##increment=-0.6 # Vgate-Vth

##tstart=100

##tend

Tempcontrol=0

#temperature=300

#print("Temperature")

def set_drain_voltage(left=-0.36,right=-0.2,target=-0.05):

    xnm2=left

    xnm1=right



    voltsource.set_voltage_a(xnm1)

    foo1=meter.read_voltage()

    f1=foo1-target



    voltsource.set_voltage_a(xnm2)

    foo2=meter.read_voltage()

    f2=foo2-target



    target_diff=[]

    voltage_a_set=[]



    for iteration in range(8):



	###

	voltsource.set_voltage_a(xnm1)

	time.sleep(1)

	foo1=meter.read_voltage()

	f1=foo1-target

	target_diff.append(abs(f1))

	voltage_a_set.append(xnm1)



	###

	if not f1==f2:

    	    xn= xnm1-(f1*(xnm1-xnm2)/(f1-f2))

	else:

	    xn=xnm1



	print iteration,xnm1,foo1,xn,f1,f2



	if xn<left:

	    print "voltage outside of bounds: resetting"

	    xn=left



	if xn>right:

	    print "voltage outside of bounds: resetting"

    	    xn=right



	xnm2=xnm1

	xnm1=xn

	f2=f1



    xnm2_temp = voltage_a_set[0]

    foo1_temp = target_diff[0]



    for diff,voltage in zip(target_diff,voltage_a_set):



        if diff<foo1_temp:



            foo1_temp=diff

            xnm2_temp=voltage





    voltsource.set_voltage_a(xnm2_temp)

    time.sleep(100)

    foo1=meter.read_voltage()

    xnm2=xnm2_temp



    #print "Vdrain=%s, Vsupply= %s" % (foo1,xnm2) #>>$dir/current

    print "      " #>>$dir/current

    return (foo1,xnm2)



    #### end midpoint





##def voltage_convert(voltin,multimeter,VDS):

##    current=(voltin-multimeter)/1000.

##    R=multimeter/current

##    voltout=(R+1000)/R*VDS

##    return voltout



def convert1(freq_span,amplFact,fg_spectrum,bg_spectrum):
    f=0
    fstep=freq_span*1000./400
    lognoise=[]
    logf=[]
    logfdata=[]
    #logbdata=[]
    i=1
    for fgdata,bgdata in zip(fg_spectrum,bg_spectrum):
        if (i<400):
            fdata=fgdata/amplFact
            bdata=bgdata/amplFact
            noise=fdata*fdata-bdata*bdata
#            print f,noise




            if (noise>1e-16 and f>0 and abs(f-60)>0 and  noise<1e-4 and abs(f-120)>3 and abs(f-180)>3 and abs(f-240)>3 and abs(f-300)>3 and abs(f-360)>3 and abs(f-420)>3 and abs(f-480)>3 and abs(f-540)>3 and abs(f-600)>3 and abs(f-660)>3 and abs(f-720)>3 and abs(f-780)>3 and abs(f-840)>3 and abs(f-900)>3 and abs(f-960)>3):

                lognoise.append(math.log10(noise))
                logf.append(math.log10(f))
                logfdata.append(math.log10(fdata))




            f=f+fstep
    return((logf,lognoise,logfdata))


##tempcon=cryocon34.cryocon34(e5810_addr,12)


##while temperature <= tend:



# temperature settings



##    tempcon.write("*RST")

##    print "Current Temperature",

##    print tempcon.get_tempK()

##    print "setting temperature"

##    tempcon.set_tempK(temperature)

##    print "waiting"

##    tempcon.wait_tempK(temperature)

##

##    print "Temperature goal achieved: %s K \n" % temperature

##    print "Wait 40 seconds...\n"

##    time.sleep(40)
print 'test'


if automeasure==1:

    device='Diode3_HighSpeed'

    numbAve=6000 #!5000-6000 or 8000 if noise data are not good

    amplFact=200 #!check preamplifier

    freqSpan=11 # 8:48.75Hz;9:97.5Hz;10:195Hz;11:390Hz;12:780Hz;13:1.01kHz(1.56kHz);14:3.125Hz;15:6.25Hz;16:12.5kHz;17:25kHz;18:50kHz;19:100kHz


   # temperature=float(raw_input())
    #vth=-3.08537+temperature*(-0.0002909)
    #vth=-2.30134+temperature*(-0.00107)
    #vth=-2.967
    #vth=-3.93448+temperature*0.0003485
    #vth=-3.11472+temperature*0.00037
    #vth=-2.13745+temperature*(-0.0016)
    #vth=-2.294

    #gateincrement=[20]


    #print 'increment', increment

else:

    print("Temperature")

    temperature=float(raw_input())

    print("Device name")

    device=raw_input()

    print("numb ave")

    numbAve=int(raw_input())

    print("amplFact")

    amplFact=float(raw_input())

    print("freqSpan: (Devided by 2)\n  0.39kHz -- input:11\n 0.78kHz -- input: 12\n")

    freqSpan=float(raw_input())

    print("vth")

    vth=float(raw_input())
    print ("increment:")
    increment=float(raw_input())



if (freqSpan==19):

    freq_span=100  #100kHz

elif (freqSpan==18):

    freq_span=50  #50kHz

elif (freqSpan==17):

    freq_span=25  #25kHz

elif (freqSpan==16):

    freq_span=12.5  #12.5kHz

elif (freqSpan==15):

    freq_span=6.25  #6.25kHz

elif (freqSpan==14):

    freq_span=3.125  #3.125kHz

elif (freqSpan==13):

    freq_span=1.01 #1.01kHz #1.56kHz

elif (freqSpan==12):

    freq_span=0.78  #780Hz

elif (freqSpan==11):

    freq_span=0.39  #11

elif (freqSpan==10):

    freq_span=0.195  #10

elif (freqSpan==9):

    freq_span=0.0975  #9

elif (freqSpan==8):

    freq_span=0.04875  #8

elif (freqSpan==7):

    freq_span=0.0244  #7

elif (freqSpan==6):

    freq_span=0.0122  #6

else:

    print("freqspan: (kHz)")

    freq_span=float(raw_input())

#increment=0.07


    #vth=0.08909 #EN25-3
   #! vth=0.00701 # EN27-3  -- without Gate dependence
    #vth=-5.7E-4*temperature+0.05383

    #vth=64  #for S7E37&S7E5

   #! gateincrement=[0.4] -- without Gate dependence
    #increment=0.4


##  voltsource.set_voltA(1.0)

   # if (temperature==100 or temperature==150 or temperature==200 or temperature==300 or temperature==400):
    #    print "Beginning gate dep"
    #    gateincrement=[0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.8,1.0,1.2,1.5]

print "Beginning gate dependence"

vth=0
#vth=-0.007 #put the real Vth

gateincrement=[0]
#gateincrement=[0.07]
#gateincrement=[0.05,0.07,0.1,0.13,0.2,0.3,0.4,0.5,0.7,0.9,1]
#gateincrement=[0.07,0.1,0.07,0.1,0.07,0.1,0.2,0.3,0.4,0.5,0.7,0.4,0.5,0.7,0.4,0.5,0.7,0.9,0.9]
#gateincrement=[0.2,0.3,0.4,0.5,0.6,0.2,0.3,0.4,0.5,0.6,0.2,0.3,0.4,0.5,0.6]

    #gateincrement=[-10,0,10,20,30,40,50,60,70,80,80,100]

    #gateincrement=[-80, -70, -60, -40, -30, -20, -10, 0, 10,20,30,40,50,60,80]
    #gateincrement=[-90]
#

#   if (temperature==251 or temperature==30 or temperature==206 or temperature==401):
#     print "Beginning gate dep"

    #vth=-3.74

    #gateincrement=[0.2,0.3,0.4,0.5,0.7,0.8,1,1.2,1.5]
     #gateincrement=[0.2,0.3,0.4,0.5,0.7,0.8,1,1.2,1.5]

for increment in gateincrement:

    #vth=48.05+temperature*(-0.088)

    Vgate=vth+increment

    print "vth=", vth

    print 'increment', increment

    print "setting gate voltage: %s" % Vgate


    #voltsource2.set_voltage_b(Vgate)

    ##    voltsource.set_voltA(1.0)
#    vdrain=0
#    vsupply=0
    #vdrain,vsupply=set_drain_voltage(left=0,right=10,target=0.05)
    ##vdrain,vsupply=set_drain_voltage(left=vdd_l8t,ri5=vdd_right,target=drain)


    ##voltsource.set_output(1)

    print "Finished outut."

    ##    time.sleep(5)

    ##    VDS=meter.read_voltage()

    ##    VA=voltage_convert(1,VDS,0.1)

    ##    print "VDS: %s   VA: %s" % (VDS,VA)

    ##    voltsource.set_output(0)

    ##    voltsource.set_voltA(VA)

    ##    voltsource.set_output(1)



#    time.sleep(60) #!increase to 60-90 - wait for setting up voltage
    print "Set gate and drain voltage with PA"
    time.sleep(20) #!increase to 60-90 - wait for setting up voltage
    print "Starting noise measurement"

    #A=meter.read_voltage()

    #print "VDS: %s" % A



    SA.setup(numbAve,freqSpan)



#    time.sleep(60) #!increase to 60-90 - wait after calibrating SA!!!
    time.sleep(10) #!increase to 60-90 - wait after calibrating SA!!!




    print "Finished SR 760 calibration."



    SA.start()

    SA.wait()

#    time.sleep(120) #!increase to 60-90 - wait after averaging
    time.sleep(10) #!increase to 60-90 - wait after averaging

    fg_spectrum=SA.read_spectrum()

    print "Finished Fg noise measurement."




    print "Set drain to 0V NOW"
    time.sleep(20)
    print "Starting background measurement"

    #time.sleep(5)

    SA.setup(numbAve,freqSpan)

    time.sleep(40)



    SA.start()

    SA.wait()

#    time.sleep(120)
    time.sleep(10)

    bg_spectrum=SA.read_spectrum()

    print "Finish Bg noise measurement."



    logf,logn,logfdata=convert1(freq_span,amplFact,fg_spectrum,bg_spectrum)






    deviceinfo='%s_Vgate=%s_inc=[%s]_fs=%skHz_vd=%s' % (device,Vgate,increment,freq_span,vdrain)
    rawinfo='%s_Vg=%s' % (device,Vgate)
    ff=open(deviceinfo+'noisedata.txt','w')
    ff.write('log(f) log(Svd) log(fdata)\n')
    for x,y,z in zip(logf,logn,logfdata):
        ff.write('%s %s %s\n' % (x,y,z))
    ff.close


    # Get fitting area
    #    print("X_Lower")
    #    Vlower=float(raw_input())
    #    print("X_Upper")
    #    Vupper=float(raw_input())
    Vlower=0
    Vupper=2.5
    x=[];y=[]

    for f,n,fdata in zip(logf,logn,logfdata):
        if Vlower<=f<=Vupper:
            x.append(f)
            y.append(n)

    #    print x
    #    print y
    #Linear regression using stats.linregress
    (a_s,b_s,r,tt,stderr)=scipy.stats.linregress(x,y)
    print('Linear regression using stats.linregress')
    print('regression: a=%.2f b=%.2f, std error= %.3f\n' % (a_s,b_s,stderr))

    #g=Gnuplot.Gnuplot()

    #d1=Gnuplot.Data(logf,logn)

    #g('set style data points')
    #g('set nologscale\n')
    #g('set xlabel "f(Hz)"\n')
    #g('set ylabel "Svd(V^2/Hz)"\n')
    #g.plot(d1)



    # Second plot
    #d1=Gnuplot.Data(logf,logn)
    #d2=Gnuplot.Func('%s*x+%s' % (a,b_s))
    #g('set style data points')
    #g('set nologscale\n')
    #g('set xlabel "f(Hz)"\n')
    #g('set ylabel "Svd(V^2/Hz)"\n')
    #g('set xrange [0.6:2.7]')
    #g.plot(d1,d2)
    #g.hardcopy(rawinfo+'_plot.png',terminal = 'png')
    n10=a_s+b_s
    k1=math.pow(10,b_s)
    k10=math.pow(10,n10) # noise at 10 Hz
    k11=k10*10/temperature # Svd*f/T
    n100=a_s*math.log10(100)+b_s
    k1=math.pow(10,b_s)
    k100=math.pow(10,n100) # noise at 100 Hz
    k101=k100*100/temperature # Svd*f/T
    s=abs(a_s)
    print "a=%s\tb=%s\tk10=%s\tk100=%s\t s=%s\n" % (a_s,b_s,k10,k11,s)
    #print device, s, b_s, n100, Vgate

    fl=open("T_Incre_a_b.txt","a")
    #    fl.write('fitting parameters ax+b\n')
    fl.write('%s\t %s\t %s\t %s\t %s\t %s\t %s\n' % (str(Vgate),str(vdrain),str(a_s),str(b_s),str(k10),str(k100),str(vsupply)))
    fl.close()
    f2=open("T_Incre_S_SvdT.txt","a")
    f2.write('%s\t %s\t %s\t %s\t %s\n' % (str(Vgate),str(increment),str(s),str(k11),str(k101)))
    f2.close()


    import numpy as np
    import matplotlib.pyplot as plt


    plt.scatter(logf, logn)
    plt.xlabel('f (Hz)')
    plt.ylabel('Svd(V^2/HZ)')

    #plt.show()



#    plt.hold(True)

    logf = np.linspace(0, 2.5)


    y1=np.dot(a_s,logf)
    y1=[i+b_s for i in y1]

    plt.plot(logf,y1,color='r')

    plt.savefig(deviceinfo+'.png')

    #plt.show()

    #plt.savefig(rawinfo+'.png')

#python d:\#Research\Tools\Python\code\python\data\noise_wo_temp.py