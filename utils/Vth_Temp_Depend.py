
from pathlib import Path
import pandas as pd
import glob
import os
import numpy as np
from scipy.interpolate import UnivariateSpline
from tsmoothie.smoother import *
from Vth_calculation_method import Vth_2nd_deviation


#----- scan the csv files in the preset folders -----#       
def scan_csv_files(IV_folder:str):
    # Find the target folder
    folder_path = Path.cwd().joinpath('testResults', IV_folder)
    
    # Find all of the .csv files' path in the folder
    files_path = glob.glob(os.path.join(folder_path,'*.csv'))
    
    # Find all of the .csv files' name in the folder
    file_names = [file.name for file in folder_path.glob('*.csv')]
    
    return files_path,file_names

#----- store the Temp, Vth values in the dictonary -----#
def calculate_Vth(IV_folder:str):
    Vth_data = {}
    #scan all the csv files and their pathes
    files_path, file_names = scan_csv_files(IV_folder)
    
    #extract Temperature from the file names
    T = [int(file.split('_')[1].replace('K','').replace('k','')) for file in file_names]
    #calculate the Vth value 
    Vth = [Vth_2nd_deviation(pd.read_csv(path)) for path in files_path]
    
    #Sorted the (Temp, Vth) from low temp to higher temp
    paired = zip(T,Vth)
    sorted_pairs = sorted(paired, key=lambda x:x[0])
    new_T, new_Vth = zip(*sorted_pairs)
    Vth_data['Temperature'] = list(new_T)
    Vth_data['Vth'] = list(new_Vth)
    
    return Vth_data

#----- This function is used to get the Vth value and interpolate the Vth value as the temperature step   -----#
def interpolation_Vth(IV_folder:str,temperature_step:int):
    # get the calculated Vth value and corresponding Temperature 
    T = calculate_Vth(IV_folder)['Temperature']
    Vth = calculate_Vth(IV_folder)['Vth']
    
    #Interpolation Temp and Vth based the temperature_step
    new_T = np.linspace(T[0], T[-1], int((T[-1] - T[0])/temperature_step) + 1)
    new_vth =  UnivariateSpline(T, Vth,s = 0)
    
    interpolate_vth = {'Temp':[], 'Vth':[]}
    interpolate_vth['Temp'] = new_T
    interpolate_vth['Vth'] = [round(Vth,3) for Vth in new_vth(new_T)]
    
    return interpolate_vth

def main():
    Vth = calculate_Vth('Noise_IV')
    Vth_i =interpolation_Vth('Noise_IV', 5)
    print(Vth_i)
    
if __name__ == '__main__':
    main()
