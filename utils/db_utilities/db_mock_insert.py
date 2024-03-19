import pg_sql_insert as psi
from pathlib import Path
import pandas as pd
from datetime import datetime


if __name__ == "__main__":
    wafer_info = 'W8R3C9'
    device_num = '2'
    device_width = 4000
    device_length = 300

    dose = '100K'
    test_date_time_str = '03/31/23 18:50:24'
    test_date_time = str(datetime.strptime(test_date_time_str, '%m/%d/%y %H:%M:%S').replace(tzinfo=None))
    pwd = Path.cwd().joinpath()
    filepath = pwd.joinpath('mock_data', '100K', '1_TGATE_N1_01_M1_W8R3C9_W4000L300_100k_ON20230331_185024.csv')
    
    df_iv = list(pd.read_csv(filepath).itertuples(index=False))
    # for row in df_iv:
    #     print(row)
    #     sql = f"""
    #         INSERT INTO raw_iv_data (device_num, wafer_info, device_width, device_length, dose, test_datetime,
    #         gate_voltage, drain_current, gate_current, source_current, body_current, drain_voltage)
    #         VALUES ('{device_num}', '{wafer_info}', '{device_width}', '{device_length}', '{dose}', '{test_date_time}',
    #         '{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}');
    #     """
    #     # print(f)
    #     ret = psi.pg_query(sql)

    df_iv_pad = pd.read_csv(filepath)
    df_iv_pad = df_iv_pad.assign(device_num=device_num, wafer_info=wafer_info, device_width=device_width, device_length=device_length, dose=dose, test_datetime=test_date_time)
    print(df_iv_pad)
    df_iv_pad = df_iv_pad[['device_num', 'wafer_info', 'device_width', 'device_length', 'dose', 'test_datetime', 'gate_voltage', 'drain_current', 'gate_current', 'source_current', 'body_current', 'drain_voltage']]
    print(df_iv_pad)

    psi.insert_raw_iv(df_iv_pad, 'raw_iv_data' )