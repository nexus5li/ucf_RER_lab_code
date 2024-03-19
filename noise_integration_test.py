import pandas as pd

from instruments.k2410.keithley2410 import keithley2410
from instruments.k2410.ivSweep import ivsweep_1terminal
from instruments.sr760.SR760 import SR760, sr760_self_test
from instruments.hp4140.hp4140 import hp4140
from instruments.sdm3055.multiSDM3055 import multi_SDM3055

from utils.drain_voltage_setup import drain_voltage_setup
from utils.configAdapters import config_vxi11adapters

from parameters.noise_setup import *
# # instatiate lab instruments using ip and gpib, defined in parameters.noise_setup
connection_strs = config_vxi11adapters(instrument_GPIB_Mapping, gateway_ip)

# smu_vd = keithley2410(connection_strs['k2410'], compliance_current=20e-4)
voltage_supply = hp4140(connection_strs['hp4140'], name='voltage_supply')
spectrum_analyzer = SR760(connection_strs['sr760'], name='spectrum')
multimeter = keithley2410(connection_strs['k2410'], compliance_current=20e-4)
# multimeter = multi_SDM3055(connection_strs['sdm3055'], name='multimeter')

############# Test Every Instrument #############
# # Test k2410 smus
# ivsweep_1terminal(smu_vd, 0, 5, 0.5)

# # Test spectrum analyzer
# sr760_self_test(spectrum_analyzer)

# # Test multimeter
# multimeter.read_voltage()

# Test voltage 
# voltage_supply.reset()
# voltage_supply.set_voltage_b(drain_voltage=20)
# voltage_supply.set_voltage_a(gate_voltage=3)


# # Test set_voltage using hp4140, multimeter and k2410
# target_vd = 0.5
# drain_voltage_setup(target_Vd=target_vd, Vd_delta=1e-3, 
#                     voltsource=voltage_supply.set_voltage_b, measure_vd=multimeter.read_voltage)


# # ############# Test Noise Fixed Temperature (High Power w/ 4140 for VG, 2410 for VD) #############
# def sr760_measure_spectrum(spectrum_analyzer:SR760, numAvg, freqSpan, startFreq):
#     spectrum_analyzer.setup(numAvg, freqSpan, startFreq)
#     spectrum_analyzer.start_data()
#     spectrum_analyzer.wait()
#     data = spectrum_analyzer.read_spectrum()

#     spectrum_analyzer.setup(numAvg, freqSpan, startFreq)
#     spectrum_analyzer.start_data()
#     return data


# def noise_measurement_per_step(vg, voltage_supply_func_gate: callable, 
#                                target_vd, vd_delta, vd_default, voltage_supply_func_drain: callable, voltage_measure_func:callable,
#                                numAvg, freqSpan, startFreq):
#     voltage_supply_func_gate(vg)
#     voltage_supply_func_drain(vd_default)
#     drain_voltage_setup(target_Vd=target_vd, vd_delta=vd_delta, voltsource=voltage_supply_func_drain, measure_vd=voltage_measure_func)
#     spectrum_data = sr760_measure_spectrum(spectrum_analyzer, numAvg, freqSpan, startFreq)
#     return spectrum_data

# # # Test spectrum measurement with hard coded inputs
# vg_steps = [3, 4, 5]
# vd = 0.05
# vd_default = 50
# vd_delta = 1e-3
# res = {key: pd.DataFrame() for key in vg_steps}
# for vg in vg_steps:
#     voltage_supply.reset()
#     res[vg] = noise_measurement_per_step(vg, voltage_supply.set_voltage_a, 
#                                vd, vd_delta, vd_default, voltage_supply.set_voltage_b, multimeter.read_voltage, 
#                                100, 11, 1)

# print(res)