from instruments.k2410.keithley2410 import keithley2410

import time
import pandas as pd
from datetime import datetime


def idvgSweep(smu_vg: keithley2410, smu_vd: keithley2410, vd, vg_start, vg_stop, vg_step):
    iv_measurements = {'vg': [], 'vd': [], 'ig': [], 'id': []}
    
    ########### SMU config ###########
    # Make sure all outputs are OFF
    smu_vg.disable_source()
    smu_vd.disable_source()
    # Write test_mode and the compliance_current 
    smu_vg.apply_voltage(compliance_current=1e-1)
    smu_vd.apply_voltage(compliance_current=1e-3)
 
    # set source_delay
    smu_vg.source_delay('5e-3')
    smu_vd.source_delay('5e-3')
    # set output data format
    smu_vg.format_data("ASCII")
    smu_vd.format_data("ASCII")
    smu_vg.set_null_feed('ON')
    smu_vd.set_null_feed('ON')
    # set up voltage to 0
    smu_vg.source_voltage = 0
    smu_vd.source_voltage = 0
    print('Initialization Finish')


    ########### VD,VG sweep ###########

    #set output switch to ON
    smu_vg.enable_source()
    smu_vd.enable_source()
    smu_vd.source_voltage = vd


    vg = vg_start
    if vg_step > 0:
        while vg <= vg_stop:
            smu_vg.source_voltage = vg
            time.sleep(0.01)
        
            #read data
            smu_vg.measure_current(nplc=1.1)
            smu_vg.measure_voltage(nplc=1.1)
            smu_vd.measure_current(nplc=1.1)
            smu_vd.measure_voltage(nplc=1.1)
            vg,ig = smu_vg.voltage,smu_vg.current
            vd,id= smu_vd.voltage,smu_vd.current
            
            #store data
            iv_measurements['vg'].append(vg)
            iv_measurements['ig'].append(ig)
            iv_measurements['vd'].append(vd)
            iv_measurements['id'].append(id)
            
            vg+=vg_step
            
    elif vg_step < 0:
        while vg >= vg_stop:
            smu_vg.source_voltage = vg
            time.sleep(0.01)
            
            #read data
            smu_vg.measure_current(nplc=1.1)
            smu_vg.measure_voltage(nplc=1.1)
            smu_vd.measure_current(nplc=1.1)
            smu_vd.measure_voltage(nplc=1.1)
            vg,ig = smu_vg.voltage,smu_vg.current
            vd,id= smu_vd.voltage,smu_vd.current
            
            #store data
            iv_measurements['vg'].append(vg)
            iv_measurements['ig'].append(ig)
            iv_measurements['vd'].append(vd)
            iv_measurements['id'].append(id)
            
            vg+=vg_step
    
    ########### Eplilog Cleanup ###########
    smu_vg.reset()
    smu_vd.reset()
    df_iv_measurements = pd.DataFrame(iv_measurements)
    currenttime = datetime.now().strftime("%Y-%m-%d-%H-%M")
    return {'test_results': df_iv_measurements, 'test_time': currenttime}
