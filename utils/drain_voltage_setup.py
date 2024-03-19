import time


def drain_voltage_setup(target_Vd:float, vd_delta:float, voltsource:callable, measure_vd:callable, max_steps=8, voltage_clamp=10):
    '''
    This function is used to set up the power supply voltage to satisfy the target drain voltage of device 
    target_Vd - objective drain voltage
    delta - tolerance error of drain voltage
    voltsource: call the power supply to apply voltage
    measure_vd: call the multimeter to read the current drain voltage
    max_steps - maximum tuning steps, optional, default value is 8
    '''
    #initial values 
    real_vd = [] #measure_vd list 
    set_vd = [] #source set voltage value list
    next_set_vd = target_Vd  * 100
    next_sup_vd = target_Vd * 80
    real_vd_delta = [] #divergence list
        
    # auxiliary functions
    def setup_and_measure():
        assert(next_sup_vd <= abs(voltage_clamp))
        assert(next_set_vd <= abs(voltage_clamp)) 
        voltsource(next_sup_Vd)  # set supply drain voltage
        set_vd.append(next_set_vd)  # add current supply drain voltage to the list
        time.sleep(2)
        real_vd.append(round(measure_vd(), 4))  # measure actual drain voltage
        real_vd_delta.append(round(target_Vd - real_vd[-1], 4))
        print("Supply: %s step: Supply voltage = %s;  Actual drain voltage = %s; Delta is %s " % (len(set_vd), set_vd[-1], real_vd[-1], real_vd_delta[-1]))

    # First voltage setup and measurement
    setup_and_measure()    
    next_set_vd = round(set_vd[-1] * target_Vd / real_vd[-1], 2)

    while len(real_vd) <= max_steps and vd_delta < abs(real_vd_delta[-1]):
        setup_and_measure()
        k = (real_vd[-1] - real_vd[-2]) / (set_vd[-1] - set_vd[-2])
        b = (set_vd[-1] * real_vd[-2] - set_vd[-2] * real_vd[-1]) / (set_vd[-1] - set_vd[-2])
        next_sup_Vd = round((target_Vd - b) / k, 3)

    print("Final drain voltage is %sV, supply voltage is %sV" % (real_vd[-1], set_vd[-1]))
