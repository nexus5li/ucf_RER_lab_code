from pathlib import Path

from pymeasure.adapters import VXI11Adapter
from pymeasure.adapters import VISAAdapter
import time
from instruments.sdm3055.multiSDM3055 import multiSDM3055
from instruments.k2410.keithley2410 import keithley2410
from instruments.k2410.idvgSweep import idvgSweep
from instruments.k2410.ivSweep import ivsweep_1terminal, ivsweep_two_terminals,ivsweep_output
from utils.resultsDump import save_results

# e5810a = VXI11Adapter("TCPIP::169.254.58.10::gpib0,24::INSTR")
# e5810b= VXI11Adapter("TCPIP::169.254.58.10::gpib0,25::INSTR")
# smu_vg = keithley2410(e5810a, compliance_current=20e-4)
# smu_vd = keithley2410(e5810b, compliance_current=50e-2)


# Test 2 terminal flexiable
# res = ivsweep_two_terminals([smu_vd, smu_vg], smus_sequence=['d', 'g'], fixed_voltage=3, 
#               voltageSweepStart=0, voltageSweepEnd=200, voltageSweepStep=5, wait_per_sweep=0.5)
# dump_path = Path.cwd().joinpath('testResults', 'idvgSweep')
# save_results(res['test_results'], dump_path, 'idvg_2t_testrun', res['test_time'], snapshot=False)
# print(res)

adapter = VISAAdapter("GPIB0::24::INSTR")
smu_vg = keithley2410(adapter=adapter,compliance_current=1e-1)
# adapter = VISAAdapter("USB0::0xF4EC::0x1201::SDM35HBX7R0590::INSTR")
# multimeter = multiSDM3055(adapter=adapter, name='multimeter')
# Test 1 smu
res = ivsweep_1terminal(smu_vg, voltageSweepStart=0, voltageSweepEnd=3, voltageSweepStep=1e-1)

dump_path = Path.cwd().joinpath('testResults', 'idvgSweep')
save_results(res['test_results'], dump_path, 'idvg_2t_testrun', res['test_time'], snapshot=False)
print(res)








# res1 = ivsweep_1terminal(smu_vg, voltageSweepStart=0, voltageSweepEnd=5, voltageSweepStep=0.5)
# dump_path = Path.cwd().joinpath('testResults', 'idvgSweep')
# save_results(res1['test_results'], dump_path, 'idvg_1t_testrun', res['test_time'], snapshot=True)
# # print(dump_path)
# print(res1)

# voltage_list = [x/100 for x in range(25)]
# smu_vg.smu_initialization()
# for voltage in voltage_list:
#     time.sleep(1)
#     smu_vg.reset_and_set_voltage(voltage)
#     time.sleep(1)
#     smu_vg.measure_voltage(nplc=1)
#     print(smu_vg.voltage)
