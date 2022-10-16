from sqlalchemy import create_engine
import json
from common_functions import *

def get_connection(env='dev'):
    '''
        additional checks to do:
        add try/except block
        add max 3 try's in case of failure
        add logger
    '''
    config_info = get_config_data(env)

    host = config_info['host']
    db_name = config_info['db_name']
    port = config_info['port']
    user_id = config_info['user_id']
    password = config_info['password']
    
    url = f'postgresql://{user_id}:{password}@{host}:{port}/{db_name}'

    sql_conn = create_engine(url=url)
    #for i in sql_conn.execute('select current_date'): print(i)
    return sql_conn

def execute_sql(db_conn_obj, sql): return db_conn_obj.execute(sql)
