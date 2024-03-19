from pymeasure.instruments import Instrument
from pymeasure.adapters import VXI11Adapter
import time

class SR760(Instrument):
    def setup(self, numAvg:int, freqSpan:int, startFreq:int):
        # Reset SR760 and Stop obtaining data
        self.write('*RST\n')
        self.write('STOP\n')
        
        #Set up freq span and starting freq
        self.write(f'SPAN {freqSpan}\n' )
        self.write(f'STRF {startFreq}\n')
        
        self.write('ACTG 0\n') #Active Trace 0
        self.write('MEAS 0,1\n') # Measure Power Spectrum Density(PSD) (0) for Trace 0
        self.write('DISP 0,0\n') #LogMag display for 0, 1 is for Linear Mag, 4 is for Phase and Trace is 0
        self.write('UNIT 0,1\n') #0 for Volts Pk, 1 for Volts RMS, 2 for dBV, 3 for dBVrms and Trace is 0
        self.write('WNDO 0,2\n') # Uniform for 0, Hanning for 2 and Trace is 0
        
        self.write('ISRC 0\n') #Set Input to A(0) or A-B (1)
        self.write('IGND 0\n') #Set Input Grounding to Float(0) and Ground(1)
        self.write('AUTS 0\n') #Set AutoScale for Trace 0
        
        self.write('AOFM 0\n') #OFF(no calibrations for 0), ON(Auto Calibrations)
        self.write('AOFF 0\n') #Set Auto OFFSET
        
        # Averaging the measure data
        self.write('AVGO1') #1 for turn on averaging and 0 for turn off 
        self.write(f'NAVG {numAvg}\n')  #set number of averaging
        self.write('AVGT0\n') # set averagig type, 0 for RMS, 1 for vector, 2 for peak hold
    
    def start_data(self):
        self.write('STRT\n') # start data acquisition
        
    def stop_data(self):
        self.write('STCO\n') #stop data acquisition
        
    def read_spectrum(self):
        data = {'freq_spectrum':[], 'density_spectrum':[]}
        
        for i in range(400):
            self.write(f'BVAL?0, {i}\n') # Query the value of bin i of trace 0
            trace = self.values('READ?')
            data['freq_spectrum'].append(float(trace[0]))
            self.write(f"SPEC?0, {i}\n")
            trace = self.values('READ?')
            data['density_spectrum'].append(float(trace[0]))
        return data

    def wait(self):
        while True:
            time.sleep(1)
            status = int(self.status)
            if status == 1 or status == 2:
                return
            
# e5810a= VXI11Adapter("TCPIP::169.254.58.10::gpib0,10::INSTR")   
# SA = SR760(e5810a,'Spectrum')

def sr760_self_test(sr760: SR760):
    sr760.setup(100, 11, 1)
    sr760.start_data()
    sr760.wait()
    print('download')
    data = sr760.read_spectrum()
    print(data)
    
    sr760.setup(100, 11, 1)
    sr760.start_data()
    
    
# if __name__ =="__main__":
#     main()
        
        
        
        
        
             
        
        
        
        