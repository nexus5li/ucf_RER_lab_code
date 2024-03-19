from pymeasure.adapters import VXI11Adapter
from pymeasure.instruments import Instrument
from k2410 import keithley2410

e5810a= VXI11Adapter("TCPIP::169.254.58.10::gpib0,24::INSTR")
e5810b= VXI11Adapter("TCPIP::169.254.58.10::gpib0,25::INSTR")
k2410 = keithley2410(e5810a)
#k2410.write(":source1:clear:auto ON")
#instr1 = Instrument(e5810a,"test1")
# instr2 = Instrument(e5810b,"test2")
k2410.apply_voltage()
k2410.source_voltage=10
k2410.compliance_current = 1e-5
k2410.enable_source()
k2410.measure_current()
print(k2410.current)
k2410.reset()



'''class k2410(Instrument):
    def test_write(self, voltage_val):
        self.write(f":source:volt {voltage_val}")


instr1 = k2410(e5810a, "test1")
instr2 = k2410(e5810b, "test2")
instr1.test_write(0.7)
instr2.test_write(0.5)
instr1.write(":source:volt 0.58")
# instr2.write(":source:volt 0.49")'''