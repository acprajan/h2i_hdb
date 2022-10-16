import requests
import db_conn
import json
from common_functions import *

logger = get_logger()

def get_insert_statement(table_name, json_data):
    '''
        Prepares the insert statement for DB load.
        Note:   Can be changed to merge statement to  handle update and insert. 
                However current process truncates the whole table before loading.
    '''
    sql_string = f'''insert into {table_name} ( '''
    sql_string_keys = ''''''
    sql_string_values = ''''''
    for key in json_data.keys():
        if sql_string_keys != '''''': sql_string_keys += ', '
        sql_string_keys += f'{key}'
        if sql_string_values != '''''': sql_string_values += ', '
        sql_string_values += '\'' +  f'{json_data[key]}' + '\''
    sql_string += sql_string_keys + ''' ) values ( ''' + sql_string_values + ''' );\n'''
    return sql_string

if __name__ == '__main__' :
    '''
        Contains data extraction and load logic.
    '''
    # DB connection definition
    db_conn_obj = db_conn.get_connection()
    
    config_params_info = get_config_params_info()
    car_park_avail_tbl_name = config_params_info['tables']['car_park_availability']['table_name']
    car_park_info_tbl_name = config_params_info['tables']['car_park_information']['table_name']
    available_parking_url = config_params_info['source_urls']['car_park_availability']
    parking_info_url = config_params_info['source_urls']['car_park_information']

    # Extract data from API
    car_park_avail_response = requests.get(available_parking_url)
    car_park_avail_response_data = car_park_avail_response.json()
    logger.info(f'Extracting parking availability data from url - {available_parking_url}')

    truncate_sql = f'truncate table {car_park_avail_tbl_name}'
    insert_sql = ''''''

    # Truncate existing table
    db_conn.execute_sql(db_conn_obj, truncate_sql)
    logger.info(f'Truncating parking availability data from table - {car_park_avail_tbl_name}')

    # Parse response data
    for record in car_park_avail_response_data['items'][0]['carpark_data']:
        carpark_avail_info = {}
        carpark_avail_info['carpark_number'] = record['carpark_number']
        carpark_avail_info['total_lots'] = record['carpark_info'][0]['total_lots']
        carpark_avail_info['total_free_lots'] = record['carpark_info'][0]['lots_available']
        carpark_avail_info['lot_type'] = record['carpark_info'][0]['lot_type']
        carpark_avail_info['update_time'] = record['update_datetime']
        insert_sql += get_insert_statement(car_park_avail_tbl_name, carpark_avail_info)
    
    # Data Load
    logger.info(f'Loading parking availability data into table - {car_park_avail_tbl_name}')
    db_conn.execute_sql(db_conn_obj, insert_sql)
    
    car_park_info_response = requests.get(parking_info_url)
    logger.info(f'Extracting parking information data from url - {parking_info_url}')
    car_park_info_response_data = car_park_info_response.json()

    truncate_sql = f'truncate table {car_park_info_tbl_name}'
    insert_sql = ''''''

    # Truncate existing table
    db_conn.execute_sql(db_conn_obj, truncate_sql)
    logger.info(f'Truncating parking information data from table - {car_park_info_tbl_name}')

    for record in car_park_info_response_data['result']['records']:
        carpark_info = {}
        carpark_info['short_term_parking'] = record['short_term_parking']
        carpark_info['car_park_type'] = record['car_park_type']
        carpark_info['y_coord'] = record['y_coord']
        carpark_info['x_coord'] = record['x_coord']
        carpark_info['free_parking'] = record['free_parking']
        carpark_info['gantry_height'] = record['gantry_height']
        carpark_info['car_park_basement'] = record['car_park_basement']
        carpark_info['address'] = record['address']
        carpark_info['_id'] = record['_id']
        carpark_info['carpark_number'] = record['car_park_no']
        carpark_info['type_of_parking_system'] = record['type_of_parking_system']
        insert_sql += get_insert_statement(car_park_info_tbl_name, carpark_info)

    # Data Load
    db_conn.execute_sql(db_conn_obj, insert_sql)
    logger.info(f'Loading parking information   data into table - {car_park_info_tbl_name}')
