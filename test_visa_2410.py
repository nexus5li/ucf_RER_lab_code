from pymeasure.adapters import VISAAdapter
from pymeasure.instruments.keithley import Keithley2400

adapter = VISAAdapter("GPIB0::24::INSTR")
smu_vg = Keithley2400(adapter=adapter,name='K2410')
