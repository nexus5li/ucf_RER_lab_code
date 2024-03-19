import pg_sql_insert as psi
from pathlib import Path


if __name__ == "__main__":
    pwd = Path.cwd().joinpath('db_utilities')
    db_gen_query = pwd.joinpath('db_gen.sql')
    with open(db_gen_query, 'r') as f:
        text = f.read()
        sql = text

        ret = psi.pg_query(sql)
        print(ret)