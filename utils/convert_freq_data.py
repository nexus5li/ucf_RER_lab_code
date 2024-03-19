import numpy as np

def convert_freq_data(amplFact:int, f_array:list, fg_spectrum:list,bg_spectrum:list):
    #Establish the dictionary to store the data
    noise_data = {}
    noise_data['freq'] = []
    noise_data['noise'] = []
    noise_data['fdata'] = []
    noise_data['bdata'] = []
    
    # Convert 
    for freq, fgdata, bgdata in zip(f_array,fg_spectrum,bg_spectrum):
        fdata = fgdata/amplFact
        bdate = bgdata/amplFact
        # Substract Background noise 
        noise = np.power(fdata,2) - np.power(bdate,2)
        
        #Store the data in the dictionary and return 
        noise_data['freq'].append(freq)
        noise_data['noise'].append(noise)
        noise_data['fdata'].append(np.power(fdata,2))
        noise_data['bdata'].append(np.power(bdate,2))
    
    return noise_data