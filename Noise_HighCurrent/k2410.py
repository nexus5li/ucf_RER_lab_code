#!/usr/bin/python
import time,signal,math
import struct
import sys
import data_acquisition.vxi_11 as vxi_11

class e5810(vxi_11.vxi_11_connection):
    def abort(self):
	pass

def write(self,string):
	a=vxi_11.vxi_11_connection.write(self,string)
	err,sb=self.read_status_byte()

	if sb & 4:
	    a=vxi_11.vxi_11_connection.write(self,":SYST:ERR?")
	    b=vxi_11.vxi_11_connection.read(self)
	    print "offending line:",string
	    print b[2]
	    if not int(b[2].split(',')[0]) in [0]:
		sys.exit(-1)

def wait(smu):
    while True:
    	err,sb=smu.read_status_byte()
    	time.sleep(0.001)
    	if sb & 16:
    	    break

def smu_setup(smu):
    smu.write(":route:terminals front")  # turn on the front jacks
    smu.write(":system:rsense off") #off=2-wire, on=4-wire
    smu.write(':syst:beep:state off')
    smu.write(':trace:clear')
    smu.write(":sense:current:nplc 1.0") # 1.0
    smu.write(":sour:del 0.02")  # 0.02
    smu.write(':source2:ttl 0')
    smu.write(':sense:function:concurrent on')

def trigger_shutter(smu):
    smu.write(':source2:ttl 0')
    smu.write(':source2:ttl 15')
#    time.sleep(0.01)
    smu.write(':source2:ttl 0')

def smu_init(smu):
#    print "initializing smu"
    retry=0
    failure=True
    while failure and retry<5:
	failure=False
	smu.write('*rst')
	smu.write(':status:preset')
	smu.write('*cls')
	smu.write(':Stat:QUE:CLE')
	smu.write('*idn?')
	if not smu.read()[2].find('KEITHLEY INSTRUMENTS INC.,MODEL 2410')==0:
	    failure=True
	    print "Fail"
	retry+=1
    if failure==False:
	return True
    else:
	return False

def set_smu_for_monitor(smu,voltage,current_limit):
    smu.write(":source1:clear:auto on")
    smu.write(":sour:sweep:cabort late")
    smu.write(":sour:func volt")
    smu.write(":sens:func 'CURR:DC'")
    smu.write(":sour:volt:mode list")
    smu.write(":sour:list:volt %s,%s,%s,%s" % (voltage,voltage,voltage,voltage))
    smu.write(":arm:count INF")  
    smu.write(":trig:count 4")
    smu.write(":sense:current:prot %s" % current_limit)

def idvg(smu_vg,smu_vd,vd=0.05,vg=(-0.8,0.6,0.01)):
    data='idvg\n'
    datlist=[]
    smu_init(smu_vg)
    smu_init(smu_vd)
    smu_setup(smu_vg)
    smu_setup(smu_vd)
    # make sure all outputs are off
    smu_vg.write(':output off')
    smu_vd.write(':output off')

    smu_vg.write(":sense:func 'curr'")
    smu_vd.write(":sense:func 'curr'")

    smu_vd.write(':source:volt 0.0')
    smu_vg.write(':source:volt 0.0')

    smu_vd.write(':source:del 0.005')
    smu_vg.write(':source:del 0.005')

    smu_vg.write(":format:data ASCII")
    smu_vd.write(":format:data ASCII")

    smu_vg.write(":sense:current:prot 1e-4")
    smu_vd.write(":sense:current:prot 3e-2")


    smu_vg.write(':output on')
    smu_vd.write(':output on')

    smu_vg.write(':calculate2:null:state on')
    smu_vd.write(':calculate2:null:state on')


    #set vd
    smu_vd.write(':source:volt %s' % vd)
    
    start=vg[0]
    stop=vg[1]
    step=vg[2]
    
    gvolt=start
    if vg[2]>0:
	while gvolt<=stop:
	    smu_vg.write(':source:volt %s' % gvolt)
	    # set them both to read first, and wait on both
	    smu_vg.write(':read?')
	    smu_vd.write(':read?')
	    wait(smu_vg)
	    wait(smu_vd)

	    vg,ig,foo1,foo2,foo3=smu_vg.read()[2].split(',')
	    vd,idr,foo1,foo2,foo3=smu_vd.read()[2].split(',')
	
	    data+='%s %s %s %s\n' % (vg,idr,ig,vd)
	    datlist.append((float(vg),float(idr),float(ig),float(vd)))
	    gvolt+=step

    if vg[2]<0:
	while gvolt>=stop:
	    smu_vg.write(':source:volt %s' % gvolt)
	    # set them both to read first, and wait on both
	    smu_vg.write(':read?')
	    smu_vd.write(':read?')
	    wait(smu_vg)
	    wait(smu_vd)

	    vg,ig,foo1,foo2,foo3=smu_vg.read()[2].split(',')
	    vd,idr,foo1,foo2,foo3=smu_vd.read()[2].split(',')
	
	    data+='%s %s %s %s\n' % (vg,idr,ig,vd)
	    datlist.append((float(vg),float(idr),float(ig),float(vd)))
	    gvolt+=step



    smu_vd.write(':source:volt 0.0')
    smu_vg.write(':source:volt 0.0')

    smu_vg.write(':calculate2:null:state off')
    smu_vd.write(':calculate2:null:state off')

    smu_vg.write('output off')
    smu_vd.write('output off')

    return data,datlist

def vth(smu_vg,smu_vd,vgd=(0.0,6.0,0.01)):
    data='vth\n'
    datlist=[]
    smu_init(smu_vg)
    smu_init(smu_vd)
    smu_setup(smu_vg)
    smu_setup(smu_vd)
    # make sure all outputs are off
    smu_vg.write(':output off')
    smu_vd.write(':output off')

#    smu_vg.write(":sense:func:concurrent on")
#    smu_vd.write(":sense:func:concurrent on")

    smu_vg.write(":sense:func 'curr'")
    smu_vd.write(":sense:func 'curr'")

    smu_vd.write(':source:volt 0.0')
    smu_vg.write(':source:volt 0.0')

    smu_vg.write(":format:data ASCII")
    smu_vd.write(":format:data ASCII")

    smu_vg.write(":sense:current:prot 1e-6")
    smu_vd.write(":sense:current:prot 0.5")
    smu_vg.write(":sense:current:prot max")
    smu_vd.write(":sense:current:prot max")


    smu_vg.write(':output on')
    smu_vd.write(':output on')

    smu_vg.write(':calculate2:null:state on')
    smu_vd.write(':calculate2:null:state on')


    #set vd
    
    start=vgd[0]
    stop=vgd[1]
    step=vgd[2]
    
    gvolt=start
    if step>0:
	while gvolt<=stop:
	    smu_vd.write(':source:volt %s' % gvolt)
	    smu_vg.write(':source:volt %s' % gvolt)
	    # set them both to read first, and wait on both
	    smu_vg.write(':read?')
	    smu_vd.write(':read?')
	    wait(smu_vg)
	    wait(smu_vd)

	    vg,ig,foo1,foo2,foo3=smu_vg.read()[2].split(',')
	    vd,idr,foo1,foo2,foo3=smu_vd.read()[2].split(',')
	    data+='%s %s %s %s\n' % (vg,ig,vd,idr)
	    datlist.append((float(vg),float(ig),float(vd),float(idr)))
	    gvolt+=step
    if step<0:
	while gvolt>=stop:
	    smu_vd.write(':source:volt %s' % gvolt)
	    smu_vg.write(':source:volt %s' % gvolt)
	    # set them both to read first, and wait on both
	    smu_vg.write(':read?')
	    smu_vd.write(':read?')
	    wait(smu_vg)
	    wait(smu_vd)

	    vg,ig,foo1,foo2,foo3=smu_vg.read()[2].split(',')
	    vd,idr,foo1,foo2,foo3=smu_vd.read()[2].split(',')
	    data+='%s %s %s %s\n' % (vg,ig,vd,idr)
	    datlist.append((float(vg),float(ig),float(vd),float(idr)))
	    gvolt+=step

    smu_vd.write(':source:volt 0.0')
    smu_vg.write(':source:volt 0.0')

    smu_vg.write(':calculate2:null:state off')
    smu_vd.write(':calculate2:null:state off')

    smu_vg.write('output off')
    smu_vd.write('output off')

    return data,datlist


def breakdown(smu_vg,smu_vd,idr=(1e-4,2e-3,1e-4)):
    data='breakdown\n'
    datlist=[]
    smu_init(smu_vg)
    smu_init(smu_vd)
    smu_setup(smu_vg)
    smu_setup(smu_vd)

    # make sure all outputs are off
    smu_vg.write(':output off')
    smu_vd.write(':output off')

#    smu_vg.write(":sense:func:concurrent on")
#    smu_vd.write(":sense:func:concurrent on")

    smu_vg.write(":sense:func 'curr'")
    smu_vd.write(":sense:func 'volt'")

    smu_vg.write(":source:func volt")
    smu_vd.write(":source:func curr")

    smu_vg.write(':source:volt 0.0')
    smu_vd.write(':source:curr 0.0')

    smu_vg.write(":format:data ASCII")
    smu_vd.write(":format:data ASCII")

#    smu_vg.write(":sense:current:prot 1e-6")
#    smu_vd.write(":sense:volt:prot 300")
    smu_vg.write(":sense:current:prot max")
    smu_vd.write(":sense:volt:prot max")

    smu_vg.write(':output on')
    smu_vd.write(':output on')

    smu_vg.write(':calculate2:null:state on')
    smu_vd.write(':calculate2:null:state on')


    #set vd
    
    start=idr[0]
    stop=idr[1]
    step=idr[2]
    
    dcur=start
    if step>0:
        while dcur<=stop:
	    smu_vd.write(':source:curr %s' % dcur)
	    # set them both to read first, and wait on both
	    smu_vg.write(':read?')
	    smu_vd.write(':read?')
	    wait(smu_vg)
	    wait(smu_vd)

	    vg,ig,foo1,foo2,foo3=smu_vg.read()[2].split(',')
	    vd,idr,foo1,foo2,foo3=smu_vd.read()[2].split(',')
	    data+='%s %s %s %s\n' % (vg,ig,vd,idr)
	    datlist.append((float(vg),float(ig),float(vd),float(idr)))
	    dcur+=step
    if step<0:
        while dcur>=stop:
	    smu_vd.write(':source:curr %s' % dcur)
	    # set them both to read first, and wait on both
	    smu_vg.write(':read?')
	    smu_vd.write(':read?')
	    wait(smu_vg)
	    wait(smu_vd)

	    vg,ig,foo1,foo2,foo3=smu_vg.read()[2].split(',')
	    vd,idr,foo1,foo2,foo3=smu_vd.read()[2].split(',')
	    data+='%s %s %s %s\n' % (vg,ig,vd,idr)
	    datlist.append((float(vg),float(ig),float(vd),float(idr)))
	    dcur+=step

    smu_vd.write(':source:volt 0.0')
    smu_vg.write(':source:volt 0.0')

    smu_vg.write(':calculate2:null:state off')
    smu_vd.write(':calculate2:null:state off')

    smu_vg.write('output off')
    smu_vd.write('output off')

    return data,datlist


def single_vth(smu_vg,smu_vd,vgd=(3,5,0.1)):
    smu_init(smu_vg)
    smu_init(smu_vd)
    smu_setup(smu_vg)
    smu_setup(smu_vd)

    # make sure all outputs are off
    smu_vg.write(':output off')
    smu_vd.write(':output off')

#    smu_vg.write(":sense:func:concurrent on")
#    smu_vd.write(":sense:func:concurrent on")

    smu_vg.write(":sense:func 'curr'")
    smu_vd.write(":sense:func 'curr'")

    smu_vd.write(':source:volt 0.0')
    smu_vg.write(':source:volt 0.0')

    smu_vg.write(":format:data ASCII")
    smu_vd.write(":format:data ASCII")

    smu_vg.write(":sense:current:prot 1e-6")
    smu_vd.write(":sense:current:prot 0.1")
    smu_vg.write(":sense:current:prot max")
    smu_vd.write(":sense:current:prot max")


    smu_vg.write(':output on')
    smu_vd.write(':output on')

    smu_vg.write(':calculate2:null:state on')
    smu_vd.write(':calculate2:null:state on')


    #set vd

    left=vgd[0]
    right=vgd[1]

    while (right-left)>1e-4:
	mid=(left+right)/2.0

	smu_vd.write(':source:volt %s' % mid)
        smu_vg.write(':source:volt %s' % mid)
        smu_vd.write(':read?')
        wait(smu_vd)
        vd,idr,foo1,foo2,foo3=smu_vd.read()[2].split(',')
        f1=float(idr)-(1e-3)
#	print mid,f1

	if f1>0:
	    right=mid
	if f1<0:
	    left=mid
	
    smu_vd.write(':source:volt 0.0')
    smu_vg.write(':source:volt 0.0')

    smu_vg.write(':calculate2:null:state off')
    smu_vd.write(':calculate2:null:state off')

    smu_vg.write('output off')
    smu_vd.write('output off')

    return mid

def single_vth_p(smu_vg,smu_vd,vgd=(3,5,0.1)):
    smu_init(smu_vg)
    smu_init(smu_vd)
    smu_setup(smu_vg)
    smu_setup(smu_vd)

    # make sure all outputs are off
    smu_vg.write(':output off')
    smu_vd.write(':output off')

#    smu_vg.write(":sense:func:concurrent on")
#    smu_vd.write(":sense:func:concurrent on")

    smu_vg.write(":sense:func 'curr'")
    smu_vd.write(":sense:func 'curr'")

    smu_vd.write(':source:volt 0.0')
    smu_vg.write(':source:volt 0.0')

    smu_vg.write(":format:data ASCII")
    smu_vd.write(":format:data ASCII")

    smu_vg.write(":sense:current:prot 1e-6")
    smu_vd.write(":sense:current:prot 0.1")
    smu_vg.write(":sense:current:prot max")
    smu_vd.write(":sense:current:prot max")


    smu_vg.write(':output on')
    smu_vd.write(':output on')

    smu_vg.write(':calculate2:null:state on')
    smu_vd.write(':calculate2:null:state on')


    #set vd

    left=vgd[0]
    right=vgd[1]

    while abs(right-left)>1e-4:
	mid=(left+right)/2.0

	smu_vd.write(':source:volt %s' % mid)
        smu_vg.write(':source:volt %s' % mid)
        smu_vd.write(':read?')
        wait(smu_vd)
        vd,idr,foo1,foo2,foo3=smu_vd.read()[2].split(',')
        f1=-float(idr)-(1e-3)
	#print mid,f1,float(idr)

	if f1<0:
	    right=mid
	if f1>0:
	    left=mid
	
    smu_vd.write(':source:volt 0.0')
    smu_vg.write(':source:volt 0.0')

    smu_vg.write(':calculate2:null:state off')
    smu_vd.write(':calculate2:null:state off')

    smu_vg.write('output off')
    smu_vd.write('output off')

    return mid

    