from instruments.k2410.keithley2410 import keithley2410
from instruments.sdm3055.multiSDM3055 import multiSDM3055
import time
import pandas as pd
import numpy as np
from datetime import datetime

def ivsweep_1terminal(smu:keithley2410, voltageSweepStart, voltageSweepEnd, voltageSweepStep):
    iv_measurements = {'v': [], 'i': []}
    smu.smu_initialization_voltage()
    smu.enable_source()
    for sweep_voltage in np.arange(voltageSweepStart, voltageSweepEnd + voltageSweepStep, voltageSweepStep):
        smu.source_voltage = sweep_voltage
        time.sleep(0.01)
        smu_measurement(smu, iv_measurements['i'], iv_measurements['v'])

    smu.reset()
    df_iv_measurements = pd.DataFrame(iv_measurements)
    currenttime = datetime.now().strftime("%Y-%m-%d-%H-%M")
    return {'test_results': df_iv_measurements, 'test_time': currenttime}


"""
    smus[0] must be the sweeping voltage source, smus[1] is the fixed voltage source
    
    smus_sequence should be consistent with the defintion of smus, for example:
        smus = [smu_vg, smu_vd], then smus_sequence should be ['g', 'd'] to save measurements correctly
"""
def ivsweep_two_terminals(smus: list[keithley2410], smus_sequence: list[str], fixed_voltage,
            voltageSweepStart, voltageSweepEnd, voltageSweepStep, wait_per_sweep=0.01):
    iv_measurements_labels = [f"v{smu_name}" for smu_name in smus_sequence] + [f"i{smu_name}" for smu_name in smus_sequence]
    iv_measurements = {measurment_label: [] for measurment_label in iv_measurements_labels}
    for smu in smus:
        smu.smu_initialization_voltage()
        smu.enable_source()

    smus[1].source_voltage = fixed_voltage # the second smu is fixed
    for sweep_voltage in np.arange(voltageSweepStart, voltageSweepEnd + voltageSweepStep, voltageSweepStep):
        smus[0].source_voltage = sweep_voltage
        time.sleep(wait_per_sweep)
        smu_measurement(smus[0], current_measurements=iv_measurements[iv_measurements_labels[2]], voltage_measurements=iv_measurements[iv_measurements_labels[0]])
        smu_measurement(smus[1], current_measurements=iv_measurements[iv_measurements_labels[3]], voltage_measurements=iv_measurements[iv_measurements_labels[1]])

    for smu in smus:
        smu.reset()
    
    df_iv_measurements = pd.DataFrame(iv_measurements)
    currenttime = datetime.now().strftime("%Y-%m-%d-%H-%M")
    return {'test_results': df_iv_measurements, 'test_time': currenttime}




def smu_measurement(smu:keithley2410, current_measurements: list, voltage_measurements:list, nplc=1.1):
    smu.measure_current(nplc=nplc)
    current = smu.current
    smu.measure_voltage(nplc=nplc)
    voltage = smu.voltage
    current_measurements.append(current)
    voltage_measurements.append(voltage)


def ivsweep_output(smu:keithley2410, multimeter: multiSDM3055, sweep_voltage, test_time):
                   #voltageSweepStart, voltageSweepEnd, voltageSweepStep):
    iv_measurements = {'v': [], 'i': [], 'output':[], 'time': []}
    smu.smu_initialization_voltage()
    smu.enable_source()
    #for sweep_voltage in np.arange(voltageSweepStart, voltageSweepEnd + voltageSweepStep, voltageSweepStep):
    smu.source_voltage = sweep_voltage
    time.sleep(0.02)
    for i in range(test_time * 2):
        smu_measurement(smu, iv_measurements['i'], iv_measurements['v'])
        iv_measurements['output'].append(multimeter.read_DC_voltage())
        iv_measurements['time'].append(i * 0.5)
        time.sleep(0.5)
        

    smu.reset()
    df_iv_measurements = pd.DataFrame(iv_measurements)
    currenttime = datetime.now().strftime("%Y-%m-%d-%H-%M")
    return {'test_results': df_iv_measurements, 'test_time': currenttime}

