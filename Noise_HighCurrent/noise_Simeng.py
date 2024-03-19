
#!/usr/bin/python

# this file is used for high current noise measurement--By Huiqi Gong

import time
import sys
import os
import subprocess

sys.path.append('./modules/')

import math
from data_acquisition2.vxi_11 import vxi_11_connection

import k2410
import cryocon34
import voltage_supply
import multimeter
import sr760

import scipy
import scipy.stats
import numpy as np
import csv


Simulate=False

e5810_addr='129.59.93.105'
#print "increment=",increment

#os.chdir('/Users/Ricky/Desktop/Noise/')
os.chdir('/Users/wangpengfei/Desktop/TestData')

voltsource=voltage_supply.VoltageSupply(e5810_addr,gpib=24)

meter=multimeter.Multimeter(e5810_addr,PAD=18,DEVNAME='multimeter',sim=Simulate)

SA=sr760.sr760(e5810_addr,10)

automeasure=1 # set 1 for default settings, 0 to start input

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



    for iteration in range(6):



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

    time.sleep(1)

    foo1=meter.read_voltage()

    xnm2=xnm2_temp



    print "Vdrain=%s, Vsupply= %s" % (foo1,xnm2) #>>$dir/current

    print "      " #>>$dir/current

    return (foo1,xnm2)

def convert1(freq_span,amplFact,fg_spectrum,bg_spectrum):
    f=0
    fstep=freq_span*1000./400
    lognoise=[]
    logf=[]
    logfdata=[]
    i=1
    for fgdata,bgdata in zip(fg_spectrum,bg_spectrum):
        if (i<400):
            fdata=fgdata/amplFact
            bdata=bgdata/amplFact
            noise=fdata*fdata-bdata*bdata
#            print f,noise




            if (noise>1e-16 and f>5 and abs(f-60)>0 and  noise<1e-10 and abs(f-120)>3 and abs(f-180)>3 and abs(f-240)>3 and abs(f-300)>3 and abs(f-360)>3 and abs(f-420)>3 and abs(f-480)>3):

                lognoise.append(math.log10(noise))
                logf.append(math.log10(f))
                logfdata.append(math.log10(fdata))




            f=f+fstep
    return((logf,lognoise,logfdata))

print 'test'



vth=0
increment=0
Vgate=vth+increment
temperature=300
if automeasure==1:

    device='TaS2_D2_bc'

    numbAve=10000

    amplFact=200

    freqSpan=11 # 8:48.75Hz;9:97.5Hz;10:195Hz;11:390Hz;12:780Hz;13:1.56Hz;14:3.125Hz;15:6.25Hz;16:12.5kHz;17:25kHz;18:50kHz;19:100kHz

else:

    print("Device name")

    device=raw_input()

    print("numb ave")

    numbAve=int(raw_input())

    print("amplFact")

    amplFact=float(raw_input())

    print("freqSpan: (Devided by 2)\n  0.39kHz -- input:11\n 0.78kHz -- input: 12\n")

    freqSpan=float(raw_input())


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


##    voltsource.set_voltA(1.0)

vdrain,vsupply=set_drain_voltage(left=0,right=10,target=0.05)

print "Finished output."

time.sleep(5)



A=meter.read_voltage()

print "VDS: %s" % A

SA.setup(numbAve,freqSpan)

print "Finished SR 760 calibration."



SA.start()

SA.wait()

time.sleep(5)

fg_spectrum=SA.read_spectrum()

print "Finished Fg noise measurement."



voltsource.set_voltage_a(0)

#time.sleep(5)

SA.setup(numbAve,freqSpan)

time.sleep(40)



SA.start()

SA.wait()

time.sleep(5)

bg_spectrum=SA.read_spectrum()

print "Finish Bg noise measurement."


logf,logn,logfdata=convert1(freq_span,amplFact,fg_spectrum,bg_spectrum)


deviceinfo='%s_Vth=%s_Vgate=%s' % (device,vth,Vgate)
rawinfo='%s_%sK_Vg-Vth=%s' % (device,temperature,increment)
ff=open(rawinfo+'noisedata.txt','w')
ff.write('log(f) log(Svd) log(fdata)\n')
for x,y,z in zip(logf,logn,logfdata):
    ff.write('%s %s %s\n' % (x,y,z))
ff.close

Vlower=0.5
Vupper=2.5
x=[];y=[]

for f,n,fdata in zip(logf,logn,logfdata):
    if Vlower<=f<=Vupper:
        x.append(f)
        y.append(n)

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
k100=math.pow(10,n100) # noise at 30 Hz
k101=k100*100/temperature # Svd*f/T
s=abs(a_s)
print "a=%s\tb=%s\tk10=%s\tk100=%s\t s=%s\n" % (a_s,b_s,k10,k100,s)
#print device, s, b_s, n100, Vgate

fl=open("T_Incre_a_b.txt","a")
#    fl.write('fitting parameters ax+b\n')
fl.write('%s\t%s %s %s %s %s %s %s\n' % (str(temperature),str(vth),str(increment),str(a_s),str(b_s),str(k10),str(k100),str(vsupply)))
fl.close()
f2=open("T_Incre_S_SvdT.txt","a")
f2.write('%s\t%s %s %s %s %s\n' % (str(temperature),str(vth),str(increment),str(s),str(k11),str(k101)))
f2.close()






import numpy as np
import matplotlib.pyplot as plt


plt.scatter(logf, logn)
plt.xlabel('f (Hz)')
plt.ylabel('Svd(V^2/HZ)')

#plt.show()



plt.hold(True)

logf = np.linspace(0.5, 2.5)


y1=np.dot(a_s,logf)
y1=[i+b_s for i in y1]

plt.plot(logf,y1,color='r')

plt.savefig(rawinfo+'.png')

#plt.show()

#plt.savefig(rawinfo+'.png')
