from parameters.b1505_setup import *
from instruments.b1505.agilentB1505 import b1505a
from pymeasure.adapters import VISAAdapter
from utils.configAdapters import config_vxi11adapters
import pandas as pd
import numpy as np

connection_strs = VISAAdapter("GPIB0::17::INSTR")
b1505 = b1505a(connection_strs)
b1505.reset()

res = b1505.query_modules()
print(f'SMUs used: {res}')

b1505.initialize_all_smus()
for i, smu in enumerate(b1505.smu_references, start=1):
    smu.enable() # enable SMUs
    print(f'smu{i} stands for channel {smu.channel}')
b1505.data_format(21, mode=1)

# gate = b1505.smu1 
# drain = b1505.smu2
# source = b1505.GNDU  

# b1505.meas_mode('STAIRCASE_SWEEP', *b1505.smu_references, channels=[1, 3]) # MM 2,
# b1505.sweep_timing(0, 0, step_delay=0) # All default values
# b1505.sweep_auto_abort(True, post='START') # WM 2,1

# nop = 10 # vg step cnt
# nopd = 3 # vd step cnt
# gate.staircase_sweep_source('VOLTAGE','LINEAR_SINGLE','Auto Ranging',0,3,nop,0.001)


# meas = []
# vd = 1
# v_drain = []
# for i in range(nopd):
#     gate.staircase_sweep_source('VOLTAGE','LINEAR_DOUBLE','Auto Ranging',0,3,nop,0.001)
#     drain.force('VOLTAGE', 0, vd, comp=0.01) # Force Vd to a vd, vd adds by one in each iteration
    
#     vd_paddling = [vd] * nop * 2 # An awkard way to get vd, this is the approach applied in pp-200 in programming manual
#     v_drain += vd_paddling
    
#     b1505.check_errors()
#     b1505.clear_buffer()
#     b1505.clear_timer()
#     b1505.send_trigger()
#     data = b1505.read_channels_vxi()
#     print(data)
#     meas.append(data)
#     vd = vd + 1


# v_gate = []
# i_drain = []
# i_gate = []

# smu_dict = {
#     'drain': 'SMU1',
#     'gate': 'SMU2'
# }

# for mea in meas:
#     for ele in mea:
#     #     print(ele)
#         if ele[1] == smu_dict['drain'] and 'Voltage' in ele[2]:
#             v_drain.append(ele[3])
#         if ele[1] == smu_dict['drain'] and 'Current' in ele[2]:
#             i_drain.append(ele[3])
#         if ele[1] == smu_dict['gate'] and 'Current' in ele[2]:
#             i_gate.append(ele[3])
#         if ele[1] == smu_dict['gate'] and 'Voltage' in ele[2]:
#             v_gate.append(ele[3])

# print(v_gate)
# print(i_gate)
# print(v_drain)
# print(i_drain)

# aggregated_data = np.array([v_gate, v_drain, i_drain, i_gate]).T.tolist()
# res = pd.DataFrame(aggregated_data, columns=['vg', 'vd' , 'id' , 'ig'])
# print(res)