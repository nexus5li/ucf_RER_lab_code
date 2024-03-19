import psycopg2
import psycopg2.extras as extras
import pandas as pd

CONN_STR = {
    'dev': {
        "host": f"127.0.0.1",
        "port": f"5432",
        "database": f"labdb_dev",
        "user": f"labdb_dev_so",
        "password": f"53971#"
    }
}

DB_SERVER = 'dev'

def execute_values(conn, df, table):
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join(list(df.columns))

    query = """
        INSERT INTO %s(%s) VALUES %%s ON CONFLICT(vpo, operation) DO NOTHING
    """ % (table, cols)
    cursor = conn.cursor()

    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'Error: {error}')
        conn.rollback()
        cursor.close()
        return 1
    print("the df is inserted")
    cursor.close()

def pg_query(sql, server=DB_SERVER):
    """ Execute SQL query"""
    conn = None
    result = None
    try:
        # Read Database configurations
        params = CONN_STR[server]

        # Connect to PostgreSQL DB
        conn = psycopg2.connect(**params)
        
        # create a new cursor and excecute the insert statement
        cur = conn.cursor()
        cur.execute(sql)

        # Fetch the data and get status message
        print(f"Status Message {cur.statusmessage}")
        if ('SELECT' in cur.statusmessage):
            result = cur.fetchall()
        elif ('INSERT 0 1' in cur.statusmessage):
            result = True

        # commit changes made to DB, then close the communication
        conn.commit()
        cur.close()

        return result
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'Error: {error}')
        return False

    finally:
        if conn is not None:
            conn.close()


def insert_raw_iv(data_in:pd.DataFrame, table_name:str, server=DB_SERVER):

    tuples = [tuple(x) for x in data_in.to_numpy()]
    cols = "device_num, wafer_info, device_width, device_length, dose, test_datetime, \
            gate_voltage, drain_current, gate_current, source_current, body_current, drain_voltage"

    query = """
        INSERT INTO %s(%s) VALUES %%s
    """ % (table_name, cols)
    try:
        # Read Database configurations
        params = CONN_STR[server]
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        extras.execute_values(cur, query, tuples)
        conn.commit()
        print('done')
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'Error: {error}')
        return False

    finally:
        if conn is not None:
            conn.close()