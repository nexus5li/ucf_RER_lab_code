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

# voltage_supply = hp4140(connection_strs['hp4140'], name='voltage_supply')
# multimeter = keithley2410(connection_strs['k2410'], compliance_current=20e-4) # Use 2410 as the multimeter

voltage_supply.set_voltage_a(gate_voltage=5)
voltage_supply.set_voltage_b(drain_voltage=30)

# actual_drain_v = multimeter.read_voltage()

# print(actual_drain_v)