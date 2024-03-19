import db_utilities.pg_sql_insert as psi

from pathlib import Path
from datetime import datetime
import pandas as pd
import re

# Dump csv files into the raw_iv table in labdb

raw_files_path = Path("mock_data/600K")
files = []
for file_path in raw_files_path.iterdir():
    if file_path.is_file():
        files.append(file_path)

for file in files:
    filename = file.stem
    device_num = filename.split("_", 9)[0]
    wafer_info = filename.split("_", 9)[5]
    dose = filename.split("_", 9)[7]
    dimension = filename.split("_",9)[6]
    width = int(re.split('(\d+)',dimension)[1])
    length = int(re.split('(\d+)',dimension)[3])

    test_date_time = '20230331_' + filename.split("_", 9)[-1]
    test_date_time = datetime.strptime(test_date_time, "%Y%m%d_%H%M%S")
    
    df_iv_pad = pd.read_csv(file)
    df_iv_pad = df_iv_pad.rename(columns={'VG': 'gate_voltage', 'ID': 'drain_current', 'IG': 'gate_current', 'IS': 'source_current', 'IB': 'body_current', 'VD': 'drain_voltage'})
    print(df_iv_pad)
    df_iv_pad = df_iv_pad.assign(device_num=device_num, wafer_info=wafer_info, device_width=width, device_length=length, dose=dose, test_datetime=test_date_time)
    
    df_iv_pad = df_iv_pad[['device_num', 'wafer_info', 'device_width', 'device_length', 'dose', 'test_datetime', 'gate_voltage', 'drain_current', 'gate_current', 'source_current', 'body_current', 'drain_voltage']]
    psi.insert_raw_iv(df_iv_pad, 'raw_iv_data')


