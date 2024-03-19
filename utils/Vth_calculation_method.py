import numpy as np
from scipy.interpolate import splrep, splev,UnivariateSpline
from scipy.signal import savgol_filter
from tsmoothie.smoother import *

#----- Vth extract by second deviation method -----#    
def Vth_2nd_deviation(IV_data):
    #Convert Data to list and make sure the data is monotonic increase order
    VG = IV_data['VG'].tolist()
    ID = [abs(num) for num in IV_data['ID'].tolist()]
    res = all(i < j for i, j in zip(VG, VG[1:]))
    if res == False:
        VG.reverse()
        ID.reverse()
        
    # add 10001 data between VG_start and VG_end
    start = np.float64(VG[0])
    end = np.float64(VG[-1])
    
    #Define Smoother function
    smoother = ConvolutionSmoother(window_len=30, window_type='ones')
    #smooth data
    smoother.smooth(ID) # smooth_curve
    new_VG = np.linspace(start, end, 10001)
    #Define interpolation ID parameters in function 
    g_s0 = UnivariateSpline(VG, smoother.smooth_data[0],s = 0)
    #1st /second deviatio of smooth and interpolation IDVG data
    tck = splrep(new_VG, g_s0(new_VG))
    # second derivation and smooth
    data = splev(new_VG,tck, der = 2) 
    window = 800
    order = 3
    
    # smooth the second deviation of IDVG data
    y_sf = savgol_filter(data, window, order)   
    input_list = np.array(y_sf)
    
    # find the maximum point of 2nd deviatiob of IV data    
    index, = np.where(input_list == np.max(input_list))   
    Vth = round(np.float64(new_VG[index][0]),3)
    
    return Vth

#----- Vth extract by the critical value of ID -----#    
def Vth_IV(IV_data, aspect_ratio:float,critical_ID:float):
    #Convert Data to list and make sure the data is monotonic increase order
    VG = IV_data['VG'].tolist()
    ID = [abs(num) for num in IV_data['ID'].tolist()]
    res = all(i < j for i, j in zip(VG, VG[1:]))
    if res == False:
        VG.reverse()
        ID.reverse()
        
    #Define interpolation ID parameters in function 
    new_VG = np.linspace(VG[0], VG[-5], 50001)
    g_s0 =  UnivariateSpline(VG, ID,s = 0)
    
    # Find the corresponding VG of cirtical ID 
    value_min = aspect_ratio * critical_ID
    value_max = 1.001*aspect_ratio * critical_ID  
    for index, item in enumerate(g_s0(new_VG)):
        if abs(item) >= float(value_min) and abs(item) < float(value_max):   
            return new_VG[index] 