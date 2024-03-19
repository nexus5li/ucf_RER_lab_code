
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

import sr760

#import Gnuplot

import scipy.stats

import os


Simulate=False

e5810_addr='10.8.129.57'
#e5810_addr='10.8.129.254'
#e5810_addr='169.254.58.10'
#tstart=300
#tend=30
tstart=255
tend=380
#e5810_addr='169.254.58.10'
#increment= 2.68654
#print "increment=",increment

os.chdir('/Users/xunli/Desktop/40010_off_proton_T_noise/proton+1980min')

voltsource=voltage_supply.VoltageSupply(e5810_addr,gpib=24)
voltsource2=voltage_supply2.VoltageSupply(e5810_addr,PAD=15,DEVNAME='voltage supply',sim=Simulate)
meter=multimeter.Multimeter(e5810_addr,PAD=18,DEVNAME='multimeter',sim=Simulate)
x_temp = [80.0, 120.0, 150.0, 170.0, 190.0, 210.0, 230.0, 250.0, 270.0, 300.0, 340.0, 380.0]
y_vth = [-2.462652488982523, -2.5353173825524764, -2.5909529613428166, -2.632499595441204, -2.6860632806603135, -2.7417259997933283,
-2.8306303027128887, -2.954941878659326, -3.0240585723517746, -3.0838062781770224, -3.141741045943059, -3.191414271150780]
mymodel = np.poly1d(np.polyfit(x_temp, y_vth, 6))
SA=sr760.sr760(e5810_addr,10)

tempcon=cryocon34.cryocon34(e5810_addr,12)

automeasure=1 # set 1 for default settings, 0 to start input

##increment=-0.6 # Vgate-Vth

##tstart=100

##tend

Tempcontrol=0

#temperature=300

#print("Temperature")

#change Vd here: target-->
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



    for iteration in range(9):

     voltsource.set_voltage_a(xnm1)

     time.sleep(3)

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

    time.sleep(15)

    foo1=meter.read_voltage()

    xnm2=xnm2_temp



    print "Vdrain=%s, Vsupply= %s" % (foo1,xnm2) #>>$dir/current

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

            if (noise>1e-16 and f>0 and abs(f-60)>0 and  noise<1e-7 and abs(f-120)>3 and abs(f-180)>3 and abs(f-240)>3 and abs(f-300)>3 and abs(f-360)>3 and abs(f-420)>3 and abs(f-480)>3):

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

##    print "Temperature goal achieved: %s K \n" % temperature

##    print "Wait 40 seconds...\n"

##    time.sleep(40)
print 'test'

if automeasure==1:

    device='D1'

#    numbAve=10000
    numbAve=5500
    amplFact=200

    freqSpan=11
  #  freqSpan=11 # 8:48.75Hz;9:97.5Hz;10:195Hz;11:390Hz;12:780Hz;13:1.56kHz;14:3.125kHz;15:6.25Hz;16:12.5kHz;17:25kHz;18:50kHz;19:100kHz
   # suggest=11
    #temperature=float(raw_input())
    temperature=tstart
    #vth=-3.08537+temperature*(-0.0002909)
    #vth=-4.27714+temperature*(0.000982857)
    #vth=-3.96649+temperature*(-0.000624733) #85K-200K
    #vth=-0.5879+emperature*(-0.0204)+0.00006 *(temperature ** 2) - 0.00000005 * (temperature ** 3) #250K-380K
    #vth=-2.30134+temperature*(-0.00107)
    #vth=-2.967
    #vth=-3.93448+temperature*0.0003485
    #vth=-3.11472+temperature*0.00037
    #vth=-2.13745+temperature*(-0.0016)
    #vth=-2.294

    #gateincrement=[20]

    #temperature=tstart

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

    freq_span=1.56  #1.56kHz

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
    #time.sleep(150)    #high speed 90s,DIP 120-150s
    for remaining in range(150, -1, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining....".format(remaining))
        sys.stdout.flush()
        time.sleep(1)
    print '\n'
    print 'Pre Measure Temperature:', tempcon.get_tempK(),"K"
    #time.sleep(0)
    #time.sleep(5)    #high speed 90s,DIP 120-150s
    #vth=-3.13
    #vth=-4.13  #Vth from IV curve
    #vth=-0.0014*temperature-2.3574#80-160K
    #vth=-2.5159+temperature*(-0.0017) #80K-210K
    #vth=temperature*(-0.0009)+(-0.000004) * (temperature ** 2)-2.2912 #80K-210K
    #vth=(-1.1449)+(-0.0097) * temperature +(0.00001) * (temperature ** 2) #215K-380K
    #vth=-1.5894+temperature*(-0.005) #215K-270K
    #vth=(-1.5157)+(-0.0075) * temperature +(0.000008) * (temperature ** 2) #275K-380K
    #vth=-2.62502+temperature*(-0.00135)  #250K-380K
    #vth=-2.70988+temperature*(-0.000855639)  #300K-400K
    #vth=0.51135+(temperature*-7.23145E-4)
    #vth =-2.55
    vth = mymodel(temperature)
    #vth=-0.100103546+(temperature*-0.000678215)
    #vth=64  #for S7E37&S7E5
    increment=0.5
    #VG-Vth = increment   increme must be linear region
##  voltsource.set_voltA(1.0)
   # if (temperature==100 or temperature==150 or temperature==200 or temperature==300 or temperature==400):
    #    print "Beginning gate dep"
    #    gateincrement=[0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.8,1.0,1.2,1.5]
    #vth=48.05+temperature*(-0.088)

    Vgate=vth+increment

    print "vth=", vth

    print 'increment', increment

    print "setting gate voltage: %s" % Vgate

    voltsource2.set_voltage_b(Vgate)

    ##    voltsource.set_voltA(1.0)
    # change Vdd_right and target here-->
    # target = Vd_that_you_want
    # Vdd_right changes from
    vdrain,vsupply=set_drain_voltage(left=2,right=10,target=0.10)
    ##vdrain,vsupply=set_drain_voltage(left=vdd_l8t,ri5=vdd_right,target=drain)

    ##voltsource.set_output(1)

    print "Finished out."

    ##    time.sleep(5)

    ##    VDS=meter.read_voltage()

    ##    VA=voltage_convert(1,VDS,0.1)

    ##    print "VDS: %s   VA: %s" % (VDS,VA)

    ##    voltsource.set_output(0)

    ##    voltsource.set_voltA(VA)

    ##    voltsource.set_output(1)



    time.sleep(15)



    A=meter.read_voltage()

    print "VDS: %s" % A



    SA.setup(numbAve,freqSpan)



    time.sleep(15)



    print "Finished SR 760 calibration."



    SA.start()

    SA.wait()

    time.sleep(15)

    fg_spectrum=SA.read_spectrum()

    print "Finished Fg noise measurement."


    voltsource.set_voltage_a(0)

    #time.sleep(5)

    SA.setup(numbAve,freqSpan)

    time.sleep(15)



    SA.start()

    SA.wait()

    time.sleep(15)

    bg_spectrum=SA.read_spectrum()

    print "Finish Bg noise measurement."



    logf,logn,logfdata=convert1(freq_span,amplFact,fg_spectrum,bg_spectrum)



    voltsource2.set_voltage_b(0)



    deviceinfo='%s_%s_Vgate=%s_vdrain=%s' % (device,temperature,Vgate,vdrain)
    rawinfo='%s_%sK_Vg=%s' % (device,temperature,Vgate)
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
    Vlower=-0.1
    Vupper=2.5
#    Vupper=1.5
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
    fl.write('%s\t%s %s %s %s %s %s \n' % (str(temperature),str(Vgate),str(vdrain),str(a_s),str(b_s),str(k10),str(k100)))
    fl.close()
    f2=open("T_Incre_S_SvdT.txt","a")
    f2.write('%s\t%s %s %s %s %s %s\n' % (str(temperature),str(Vgate),str(increment),str(s),str(k11),str(k101),str(vsupply)))
    f2.close()






    import numpy as np
    import matplotlib.pyplot as plt


    plt.scatter(logf, logn)
    plt.xlabel('f (Hz)')
    plt.ylabel('Svd(V^2/HZ)')

    #plt.show()



    plt.hold(True)

    logf = np.linspace(0, 2.5)


    y1=np.dot(a_s,logf)
    y1=[i+b_s for i in y1]

    plt.plot(logf,y1,color='r')

    plt.savefig(deviceinfo+'.png')

    #plt.show()

    #plt.savefig(rawinfo+'.png')
    temperature=temperature+5




if (temperature>300):
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



