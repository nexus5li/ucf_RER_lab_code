import db_utilities.pg_sql_insert as psi
import psycopg2

from pathlib import Path
from datetime import datetime
import pandas as pd
import re

class VthAnalyzer:
    def __init__(self, wafer_info) -> None:
        self.wafer_info = wafer_info

    def query_db_by_device(self, dose, device_num):
        query = f"SELECT * FROM raw_iv_data WHERE wafer_info='{self.wafer_info}' AND dose='{dose}' AND device_num='{device_num}';"
        # print(query)
        params = psi.CONN_STR[psi.DB_SERVER]
        conn = psycopg2.connect(**params)
        res = pd.read_sql(query, conn)
        print(res)


if __name__ == "__main__":
    wafer_info = 'W8R3C9'
    analyzer = VthAnalyzer(wafer_info=wafer_info)
    analyzer.query_db_by_device('000k', '1')