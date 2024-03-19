from pymeasure.adapters import VXI11Adapter
from pymeasure.instruments import Instrument
from k2410 import keithley2410
import time
import pandas as pd
from pathlib import Path

e5810a= VXI11Adapter("TCPIP::169.254.58.10::gpib0,24::INSTR")
e5810b= VXI11Adapter("TCPIP::169.254.58.10::gpib0,25::INSTR")
smu_vg = keithley2410(e5810a)
smu_vd = keithley2410(e5810b)

def idvg(vd, vg_start, vg_stop, step): 
    #store data in the dict as a list 
    IV_data = {}
    IV_data['vg'] = []
    IV_data['vd'] = []
    IV_data['ig'] = []
    IV_data['id'] = []
    
    
    # Make sure all outputs are OFF
    smu_vg.disable_source()
    smu_vd.disable_source()
    
    #Write test_mode and the compliance_current 
    smu_vg.apply_voltage(compliance_current=1e-6)
    smu_vd.apply_voltage(compliance_current=1e-2)
    
    #set up voltage to 0
    smu_vg.source_voltage = 0
    smu_vd.source_voltage = 0
     
    #set source_delay
    smu_vg.source_delay('5e-3')
    smu_vd.source_delay('5e-3')
    
    #set output data format
    smu_vg.format_data("ASCII")
    smu_vd.format_data("ASCII")
    
    '''#set current compliance 
    smu_vg.compliance_current = 1e-6
    smu_vd.compliance_current = 1e-2'''
    
    #set output switch to ON
    smu_vg.enable_source()
    smu_vd.enable_source()
    
    smu_vg.set_null_feed('ON')
    smu_vd.set_null_feed('ON')
    print('Initialization Finish')
    
    #set vd & vg
    smu_vd.source_voltage = vd
    
    for vg in range(vg_start,vg_stop+step, step):
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
        IV_data['vg'].append(vg)
        IV_data['ig'].append(ig)
        IV_data['vd'].append(vd)
        IV_data['id'].append(id)
    '''vg = vg_start
    if step > 0:
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
            IV_data['vg'].append(vg)
            IV_data['ig'].append(ig)
            IV_data['vd'].append(vd)
            IV_data['id'].append(id)
            
            vg+=step
            
    elif step < 0:
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
            IV_data['vg'].append(vg)
            IV_data['ig'].append(ig)
            IV_data['vd'].append(vd)
            IV_data['id'].append(id)
            
            vg+=step
    # return parameters to initial state      
    smu_vg.reset()
    smu_vd.reset()
    
    return IV_data'''
    
def main():
    data = idvg(0.05, 5, 0, -0.5)
    df = pd.DataFrame(data)
    result_path = Path.cwd().joinpath('result','IV')
    data_file_path= result_path.joinpath('1.csv')
    df.to_csv(data_file_path, index=False)

if __name__ == '__main__':
    main()
