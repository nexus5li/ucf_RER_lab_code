from pathlib import Path
from pymeasure.adapters import VISAAdapter
from instruments.sdm3055.multiSDM3055 import multiSDM3055


adapter = VISAAdapter("USB0::0xF4EC::0x1201::SDM35HBX7R0590::INSTR")
multimeter = multiSDM3055(adapter=adapter, name='multimeter')
res = multimeter.sampling_voltage(10,6)
print(res)
